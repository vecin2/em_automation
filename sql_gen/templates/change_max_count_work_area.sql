{% set work_areas = _db.fetch.all_work_areas() %}
{% set work_area_names = work_areas.column("NAME") %}
{% set __selected_work_area = selected_work_area | suggest(work_area_names) %}
{% set work_area_id = work_areas.find(NAME=__selected_work_area) %}
UPDATE FD_WORK_AREA SET (MAX_COUNT) = ({{max_count}}) WHERE ID = {{work_area_id["ID"]}};
