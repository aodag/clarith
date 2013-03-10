<div class="entry">
    <h2 class="entry-title">${entry.date} ${h.link_to_entry(request, entry)}</h2>
    <div class="entry-control">
        <a href="${request.route_url('edit_entry', slug=entry.slug)}">Edit</a>
    </div>
    <div class="entry-description">
        ${entry.description|n}
    </div>
</div>