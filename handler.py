from flask import Blueprint, current_app, make_response, jsonify
from pywebostv.model import AudioOutputSource, Application

tv_bp = Blueprint('tv', __name__)
tv_key_bp = Blueprint('key', __name__)
tv_src_bp = Blueprint('src', __name__)
tv_audio_bp = Blueprint('audio', __name__)
tv_app_bp = Blueprint('app', __name__)


@tv_bp.route('/tv/<fn>', methods=['PUT'])
def put_fn(fn):
    fn_allow = ['off', 'on', 'ch_list']

    if fn not in fn_allow:
        return resp_msg(f'Invalid function: {fn}', 400)

    atv = current_app.tv
    if fn == 'ch_list':
        atv.get_tv_ctl().channel_list()
    elif fn == 'off':
        try:
            atv.get_system_ctl().power_off()
        except Exception as e:
            print(f"Caught an exception: {e}")
            return resp_msg(f'Failed to turn off TV', 200)
    elif fn == 'on':
        try:
            atv.turn_on()
        except:
            response = make_response(jsonify({'msg': f'Failed to turn on TV'}))
            response.status_code = 500
            return response

    return resp_msg(f'{fn} sent', 200)


@tv_key_bp.route('/key/<key>', methods=['PUT'])
def put_key(key):
    key_allow = ['up', 'down', 'left', 'right', 'ok', 'info', 'back', 'home']
    key_allow += ['volume_up', 'volume_down', 'channel_up', 'channel_down']

    if key not in key_allow:
        response = make_response(jsonify({'msg': f'Invalid key: {key}'}))
        response.status_code = 400
        return response

    atv = current_app.tv
    input_ctl = atv.get_input_ctl()
    exec(f'input_ctl.{key}()')

    return resp_data(f'{key} sent', 200)


@ tv_src_bp.route('/src', methods=['GET'])
def get_src():
    atv = current_app.tv
    srcs = atv.get_source_ctl().list_sources()
    src_labels = list(map(lambda x: x['label'], srcs))

    return resp_data(src_labels, 200)


@ tv_src_bp.route('/src/<src>', methods=['PUT'])
def put_src(src):
    print(f'src: {src}')

    atv = current_app.tv
    srcs = atv.get_source_ctl().list_sources()
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

    atv.get_source_ctl().set_source(srcs[i])
    atv.popup(f'Set source to {src}')

    return resp_msg(f'set source to {src}', 200)


@ tv_audio_bp.route('/audio', methods=['GET'])
def get_audio():
    # tv_client = current_app.tv_client
    # audio_out = tv_cntl.MediaControl(tv_client).get_audio_output()
    # print(audio_out)
    audio_out = ['tv_speaker', 'external_optical']

    return resp_data(audio_out, 200)


@ tv_audio_bp.route('/audio/<out>', methods=['PUT'])
def put_audio(out):
    atv = current_app.tv
    atv.get_media_ctl().set_audio_output(AudioOutputSource(out))
    atv.popup(f'Set audio output to {out}')

    return resp_msg(f'set audio output to {out}', 200)


@ tv_app_bp.route('/app', methods=['GET'])
def get_app():
    atv = current_app.tv
    apps = atv.get_application_ctl().list_apps()
    app_titles = list(map(lambda x: x['title'], apps))
    print(app_titles)

    return resp_data(app_titles, 200)


@ tv_app_bp.route('/app/<app>', methods=['PUT'])
def put_app(app):
    atv = current_app.tv
    apps = atv.get_application_ctl().list_apps()
    app_titles = list(map(lambda x: x['title'], apps))

    i = 0
    for a in app_titles:
        if app == a:  # or app == app_ids[i]:
            break
        i += 1

    if i == len(app_titles):
        return resp_msg(f'Invalid application: {app}', 400)

    atv.get_application_ctl().launch(Application(apps[i]))
    atv.popup(f'Set app to {app}')

    return resp_msg(f'set application to {app}', 200)


def resp_msg(msg, status_code):
    response = make_response(jsonify({'msg': msg}))
    response.status_code = status_code
    return response


def resp_data(data, status_code):
    response = make_response(jsonify({'data': data}))
    response.status_code = status_code
    return response
