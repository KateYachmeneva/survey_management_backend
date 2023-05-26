def selected_for_tree(context, run):
    """На основе выбранного рейса узнаем какие модели выбраны выше"""
    context['selected_client'] = str(run.section.wellbore.well_name.pad_name.field.client)
    context['selected_field'] = run.section.wellbore.well_name.pad_name.field.field_name
    context['selected_pad'] = run.section.wellbore.well_name.pad_name.pad_name
    context['selected_well'] = run.section.wellbore.well_name.well_name
    context['selected_wellbore'] = run.section.wellbore.get_full_wellbore_name()
    context['selected_section'] = run.section.section
    context['selected_run'] = run.run_number
