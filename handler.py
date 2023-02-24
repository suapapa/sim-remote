from flask import Blueprint, current_app, make_response, jsonify
import pywebostv.controls as tv_cntl
from pywebostv.model import AudioOutputSource, InputSource
import tv

tv_bp = Blueprint('tv', __name__)
tv_key_bp = Blueprint('key', __name__)
tv_src_bp = Blueprint('src', __name__)
tv_audio_bp = Blueprint('audio', __name__)


@tv_bp.route('/tv/<fn>', methods=['PUT'])
def put_fn(fn):
    fn_allow = ['off', 'on', 'ch_list']

    if fn not in fn_allow:
        response = make_response(jsonify({'msg': f'Invalid function: {fn}'}))
        response.status_code = 400
        return response

    tv_client = current_app.tv_client
    if fn == 'ch_list':
        tv_cntl.TvControl(tv_client).channel_list()
    elif fn == 'off':
        tv_cntl.SystemControl(tv_client).power_off()
    elif fn == 'on':
        try:
            tv.turn_on(current_app.tv_mac)
        except:
            response = make_response(jsonify({'msg': f'Failed to turn on TV'}))
            response.status_code = 500
            return response

    response = make_response(jsonify({'msg': f'{fn} sent'}))
    response.status_code = 200
    return response


@tv_key_bp.route('/key/<key>', methods=['PUT'])
def put_key(key):
    key_allow = ['up', 'down', 'left', 'right', 'ok', 'dash', 'back', 'home']
    key_allow += ['volume_up', 'volume_down', 'channel_up', 'channel_down']

    if key not in key_allow:
        response = make_response(jsonify({'msg': f'Invalid key: {key}'}))
        response.status_code = 400
        return response

    input_ctl = tv_cntl.InputControl(current_app.tv_client)
    input_ctl.connect_input()
    exec(f'input_ctl.{key}()')

    response = make_response(jsonify({'msg': f'{key} sent'}))
    response.status_code = 200
    return response


@ tv_src_bp.route('/src', methods=['GET'])
def get_src():
    tv_client = current_app.tv_client
    srcs = tv_cntl.SourceControl(tv_client).list_sources()
    src_labels = list(map(lambda x: x['label'], srcs))

    response = make_response(jsonify({'data': src_labels}))
    response.status_code = 200
    return response


@ tv_src_bp.route('/src/<src>', methods=['PUT'])
def put_src(src):
    print(f'src: {src}')

    tv_client = current_app.tv_client

    srcs = tv_cntl.SourceControl(tv_client).list_sources()
    src_labels = list(map(lambda x: x['label'], srcs))
    i = 0
    for s in src_labels:
        if src == s:
            break
        i += 1

    if i == len(src_labels):
        response = make_response(jsonify({'msg': f'Invalid source: {src}'}))
        response.status_code = 400
        return response

    tv_cntl.SourceControl(tv_client).set_source(srcs[i])

    notify_tv(f'Set source to {src}')

    response = make_response(jsonify({'msg': f'set source to {src}'}))
    response.status_code = 200
    return response


@ tv_audio_bp.route('/audio', methods=['GET'])
def get_audio():
    # tv_client = current_app.tv_client
    # audio_out = tv_cntl.MediaControl(tv_client).get_audio_output()
    # print(audio_out)
    audio_out = ['tv_speaker', 'external_optical']

    response = make_response(jsonify({'data': audio_out}))
    response.status_code = 200
    return response


@ tv_audio_bp.route('/audio/<out>', methods=['PUT'])
def put_audio(out):
    tv_client = current_app.tv_client
    tv_cntl.MediaControl(tv_client).set_audio_output(AudioOutputSource(out))

    notify_tv(f'Set audio output to {out}')

    response = make_response(jsonify({'msg': f'set audio output to {out}'}))
    response.status_code = 200
    return response

# ---


def notify_tv(msg):
    tv_client = current_app.tv_client
    tv_cntl.SystemControl(tv_client).notify(msg)
