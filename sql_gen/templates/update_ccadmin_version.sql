{% set all_releases = _db.fetch.all_releases() %}
{% set release_names =all_releases.column("RELEASE_NAME") %}
update ccadmin_version
set upgrade_version ={{upgrade_version | print(all_releases)}}
where RELEASE_NAME = '{{release_name | suggest(release_names)}}';
