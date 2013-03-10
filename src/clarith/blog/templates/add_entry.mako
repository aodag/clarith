<%inherit file="${context['main_template'].uri}"/>

<h1>${blog.title}</h1>
${h.form(request.url)}
${fs.render()|n}
${h.submit('add', 'Add')}
${h.end_form()}