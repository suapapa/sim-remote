from flask import Blueprint, current_app, make_response, jsonify
import pywebostv.controls as tv_cntl

tv_bp = Blueprint('tv', __name__)
tv_key_bp = Blueprint('key', __name__)
tv_src_bp = Blueprint('src', __name__)
tv_audio_bp = Blueprint('audio', __name__)

@tv_bp.route('/tv/<fn>', methods=['PUT'])
def put_fn(fn):
    fn_allow = ['power_off', 'power_on', 'ch_list']

    if fn not in fn_allow:
        response = make_response(jsonify({'msg': f'Invalid function: {fn}'}))
        response.status_code = 400
        return response
    
    tv_client = current_app.tv_client
    if fn == 'ch_list':
        tv_cntl.TvControl(tv_client).channel_list()
    elif fn == 'power_off':
        tv_cntl.SystemControl(tv_client).power_off()
    # elif fn == 'power_on':
    #     tv_cntl.SystemControl(tv_client).power_on()


@tv_key_bp.route('/tv/key/<key>', methods=['PUT'])
def put_key(key):
    key_allow = ['menu', 'back', 'up', 'down', 'left', 'right']
    key_allow += ['home', 'volume_up', 'volume_down', 'channel_up', 'channel_down']

    if key not in key_allow:
        response = make_response(jsonify({'msg': f'Invalid key: {key}'}))
        response.status_code = 400
        return response

    tv_client = current_app.tv_client
    tv_cntl.InputControl(tv_client).set_input(key)

    response = make_response(jsonify({'msg': f'{key} sent'}))
    response.status_code = 200
    return response

@tv_audio_bp.route('/tv/audio', methods=['GET'])
def get_audio():
    tv_client = current_app.tv_client
    audio_out = tv_cntl.MediaControl(tv_client).get_audio_output()

    response = make_response(jsonify({'data': audio_out}))
    response.status_code = 200
    return response

@tv_audio_bp.route('/tv/audio/<out>', methods=['PUT'])
def put_audio(out):
    tv_client = current_app.tv_client
    tv_cntl.MediaControl(tv_client).set_audio_output(out)

    response = make_response(jsonify({'msg': f'set audio output to {out}'}))
    response.status_code = 200
    return response

# ---

def notify_tv(msg):
    tv_client = current_app.tv_client
    tv_cntl.NotificationControl(tv_client).notify(msg)