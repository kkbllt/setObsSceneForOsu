import obspython as obs
from multiprocessing import shared_memory

defaults_scene      = ""
to_scene            = ""
playing_source_name = ""
nowText             = ""

#==================


def reload_scene():
    global defaults_scene
    global to_scene
    global playing_source_name
    global nowText

    res = shared_memory.ShareableList(name='osumemory')

    _play_state = res[1]

    def _setText(_text):
        _textsource = obs.obs_get_source_by_name(playing_source_name)
        settings = obs.obs_data_create()
        obs.obs_data_set_string(settings, "text", _text)
        obs.obs_source_update(_textsource, settings)
        obs.obs_source_release(_textsource)
        obs.obs_data_release(settings)

    nowScene = obs.obs_frontend_get_current_scene()
    nowScenename = obs.obs_source_get_name(nowScene)
    obs.obs_source_release(nowScene)
    if '_play_state' not in res or "".zfill(1024) not in res:
        _osutext = res[3]
        if nowText != _osutext:
            _setText(_osutext)
            nowText = _osutext

        if _play_state == 2 and nowScenename != to_scene:
            t_scene = obs.obs_get_source_by_name(to_scene)
            obs.obs_frontend_set_current_scene(t_scene)
            obs.obs_source_release(t_scene)
        elif _play_state != 2 and nowScenename != defaults_scene:
            d_scene = obs.obs_get_source_by_name(defaults_scene)
            obs.obs_frontend_set_current_scene(d_scene)
            obs.obs_source_release(d_scene)


def refresh_pressed(props, prop):
    reload_scene()

#==================

def script_description():
    return "OSU专用场景切换工具。\n暂停切换请卸载此脚本或者留空任意场景项"

def script_update(settings):
    global defaults_scene
    global to_scene
    global playing_source_name

    defaults_scene = obs.obs_data_get_string(settings, "defaults_scene")
    to_scene       = obs.obs_data_get_string(settings, "to_scene")
    playing_source_name = obs.obs_data_get_string(settings, "playing_source_name")

    obs.timer_remove(reload_scene)

    if "" not in (to_scene,defaults_scene):
        obs.timer_add(reload_scene, 500)

def script_properties():
    props = obs.obs_properties_create()

    pyt = obs.obs_properties_add_list(props, "playing_source_name", "选择一个text用以显示\n一些额外信息(可留空)", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sources = obs.obs_enum_sources()
    if sources is not None:
        for source in sources:
            source_id = obs.obs_source_get_unversioned_id(source)
            name = obs.obs_source_get_name(source)
            if source_id != "text_gdiplus" or source_id != "text_ft2_source":
                obs.obs_property_list_add_string(pyt, name, name)

        obs.source_list_release(sources)

    ds = obs.obs_properties_add_list(props, "defaults_scene", "默认场景", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    ts = obs.obs_properties_add_list(props, "to_scene", "新场景", obs.OBS_COMBO_TYPE_EDITABLE, obs.OBS_COMBO_FORMAT_STRING)
    sceness = obs.obs_frontend_get_scenes()
    if sceness is not None:
        for scenes in sceness:
            scens_name = obs.obs_source_get_name(scenes)
            obs.obs_property_list_add_string(ds, scens_name,scens_name)
            obs.obs_property_list_add_string(ts, scens_name,scens_name)

        obs.source_list_release(sceness)

    obs.obs_properties_add_button(props, "button", "Refresh", refresh_pressed)
    return props


obs.script_log(obs.LOG_INFO, f"run!")
