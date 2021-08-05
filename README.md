# custom_compliance_example

ncs-make-package --service-skeleton python-and-template --action-example custom_compliance_example

plan:
I usually do is to have a service and use the dry-run feature to create the reports via an action. The built-in reporting is a nice feature, but it is not flexible enough for the use cases I had to audit. (for example, execute show commands and according to the result the audit logic changes)
Having an action, you can model the result to be in any format you need and it will be returned via the API. 


pip3 install jinja2

accessing template files requires a bit of pathing using 
import os

```
admin@ncs(config)# action double number 3
Error: Python cb_action error. [Errno 2] No such file or directory: '~/nso-instance/packages/custom_compliance_example/python/custom_compliance_example/templates/wan.j2'
admin@ncs(config)#
```

join paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.path.join(BASE_DIR + rest_of_path)

from:
https://github.com/NSO-developer/service-launcher/blob/d0dc2a41315d5ac6dd8aca0d78a10b14610ff63d/web_ui/api_controller.py
DIR_PATH = os.path.dirname(os.path.realpath(__file__))
env = Environment(loader=FileSystemLoader(DIR_PATH + '/templates'))
template = env.get_template('edit_config.j2')
rendered = template.render(filter_xml=filter_xml)

def create(self, template_service_name, **kwargs):
    """
    Create a configuration object
    :param template_service_name: jinja template to be used
    :param kwargs: arguments to be replaced in the jinja template
    :return:
    """
    template = self.env.get_template(template_service_name + '.j2')
    rendered = template.render(**kwargs)
    self.send_edit_config_request(rendered)