<div class="entry">
    <h2 class="entry-title">${entry.date} ${h.link_to_entry(request, entry)}</h2>
    <div class="entry-control">
        <a href="edit">Edit</a>
    </div>
    <div class="entry-description">
        ${entry.description|n}
    </div>
</div>