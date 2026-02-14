## Tagging and Search

### Tagging
- Posts support tags through a ManyToMany relationship (`Post.tags`).
- Tags are entered as comma-separated values in the Post form (e.g. `django, python`).
- New tags are created automatically if they don’t already exist.

### Viewing posts by tag
- Visit: `/tags/<tag_name>/`  
  Example: `/tags/django/`

### Search
- Visit: `/search/?q=keyword`
- Search checks:
  - Post title
  - Post content
  - Tag names
- Implemented using Django `Q` objects for combined lookups.
