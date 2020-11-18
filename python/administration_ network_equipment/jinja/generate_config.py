# -*- coding: utf-8 -*-
"""
generate_config.
params:
* template - path (example, "templates/for.txt")
* data_dict - dict with values for pass in template
templates/for.txt data in data_files/for.yml.
"""
import yaml
from jinja2 import Environment, FileSystemLoader

def generate_config(template, data_dict):
    template_ = template.split('/')
    env = Environment(loader=FileSystemLoader(template_[0]), trim_blocks=True, lstrip_blocks=True)
    template_upload = env.get_template(template_[1])
    data_out = template_upload.render(data_dict)
    return data_out

"""
#alternative
def generate_config(template, data_dict):
    templ_dir, templ_file = os.path.split(template)
    env = Environment(
        loader=FileSystemLoader(templ_dir), trim_blocks=True, lstrip_blocks=True
    )
    templ = env.get_template(templ_file)
    return templ.render(data_dict)
"""
if __name__ == "__main__":
    path_template = "templates/for.txt"
    with open('data_files/for.yml') as file:
        devices = yaml.safe_load(file)
    generate_config(path_template, devices)

