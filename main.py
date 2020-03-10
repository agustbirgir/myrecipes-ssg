import os
import codecs
from datetime import datetime
from jinja2 import Environment, PackageLoader
from markdown2 import markdown

POSTS = {}
for markdown_post in os.listdir('content'):
    file_path = os.path.join('content', markdown_post)

    with open(file_path, 'r') as file:
        POSTS[markdown_post] = markdown(file.read(), extras=['metadata'])

POSTS = {
    post: POSTS[post] for post in sorted(POSTS, key=lambda post: datetime.strptime(POSTS[post].metadata['date'], '%Y-%m-%d'), reverse=True)
}
#template
env = Environment(loader=PackageLoader('main', 'templates'))
index_template = env.get_template('index.html')
bread_template = env.get_template('bread.html')
post_template = env.get_template('post.html')




posts_metadata = [POSTS[post].metadata for post in POSTS]
tags = [post['tags'] for post in posts_metadata]
bread_html = bread_template.render(posts=posts_metadata, tags=tags)

#forsiðan ( er ekki með MD post rendering)
index_html = index_template.render()

#forsiða
with open('../myrecipez/index.html', 'w', encoding='utf-8') as file:
    file.write(index_html)

#brauðsiða
with open('../myrecipez/bread.html', 'w') as file:
    file.write(bread_html)    

#uppskriftar
for post in POSTS:
    post_metadata = POSTS[post].metadata

    post_data = {
        'content': POSTS[post],
        'title': post_metadata['title'],
        'date': post_metadata['date'],
        'thumbnail': post_metadata['thumbnail']
    }

    post_html = post_template.render(post=post_data)

    post_file_path = '../myrecipez/posts/{slug}.html'.format(slug=post_metadata['slug'])

    os.makedirs(os.path.dirname(post_file_path), exist_ok=True)
    with open(post_file_path, 'w') as file:
        file.write(post_html)