
def root(context, missing=missing, environment=environment):
    resolve = context.resolve_or_missing
    undefined = environment.undefined
    if 0: yield None
    l_0_adquery = resolve('adquery')
    l_0_entity_def_id = resolve('entity_def_id')
    l_0_prj_prefix = resolve('prj_prefix')
    l_0_verb_name = resolve('verb_name')
    l_0_entity_ids = l_0_process_descriptor_id = l_0_process_descriptor_ref_id = missing
    t_1 = environment.filters['suggest']
    pass
    l_0_entity_ids = context.call((undefined(name='adquery') if l_0_adquery is missing else l_0_adquery), "SELECT KEYNAME FROM CCADMIN_IDMAP WHERE KEYSET ='ED'")
    context.vars['entity_ids'] = l_0_entity_ids
    context.exported_vars.add('entity_ids')
    yield to_string(t_1((undefined(name='entity_def_id') if l_0_entity_def_id is missing else l_0_entity_def_id), (undefined(name='entity_ids') if l_0_entity_ids is missing else l_0_entity_ids)))
    yield '\n'
    l_0_process_descriptor_id = ((context.call((undefined(name='prj_prefix') if l_0_prj_prefix is missing else l_0_prj_prefix)) + context.call(environment.getattr((undefined(name='entity_def_id') if l_0_entity_def_id is missing else l_0_entity_def_id), 'capitalize'))) + context.call(environment.getattr((undefined(name='verb_name') if l_0_verb_name is missing else l_0_verb_name), 'capitalize')))
    context.vars['process_descriptor_id'] = l_0_process_descriptor_id
    context.exported_vars.add('process_descriptor_id')
    template = environment.get_template('add_process_descriptor.sql', 'rewire_verb.sql')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'process_descriptor_id': l_0_process_descriptor_id, 'process_descriptor_ref_id': l_0_process_descriptor_ref_id, 'entity_ids': l_0_entity_ids})):
        yield event
    l_0_process_descriptor_ref_id = (undefined(name='process_descriptor_id') if l_0_process_descriptor_id is missing else l_0_process_descriptor_id)
    context.vars['process_descriptor_ref_id'] = l_0_process_descriptor_ref_id
    context.exported_vars.add('process_descriptor_ref_id')
    template = environment.get_template('add_process_descriptor_ref.sql', 'rewire_verb.sql')
    for event in template.root_render_func(template.new_context(context.get_all(), True, {'process_descriptor_id': l_0_process_descriptor_id, 'process_descriptor_ref_id': l_0_process_descriptor_ref_id, 'entity_ids': l_0_entity_ids})):
        yield event
    yield "\n\nUPDATE EVA_VERB \nSET (PROCESS_DESC_REF_ID) = (@PDR.%s)\nWHERE ENTITY_DEF_ID = @ED.%s AND NAME ='%s';" % (
        (undefined(name='process_descriptor_ref_id') if l_0_process_descriptor_ref_id is missing else l_0_process_descriptor_ref_id),
        (undefined(name='entity_def_id') if l_0_entity_def_id is missing else l_0_entity_def_id),
        (undefined(name='verb_name') if l_0_verb_name is missing else l_0_verb_name),
    )
