from pyramid_layout.panel import panel_config


@panel_config("entry", renderer="panels/entry_panel.mako")
def entry_panel(context, request, entry):
    return dict(entry=entry)