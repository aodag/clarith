<%inherit file="${context['main_template'].uri}"/>

<h1>${blog.title}</h1>
<p>
    ${blog.description}
</p>
<div>
    %for entry in blog.recent_entries:
        ${panel("entry", entry=entry)}
    %endfor
</div>