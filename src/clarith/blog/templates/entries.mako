<%inherit file="${context['main_template'].uri}"/>
<div>
    ${pager}
    %for entry in entries:
        ${panel("entry", entry=entry)}
    %endfor
    ${pager}
</div>