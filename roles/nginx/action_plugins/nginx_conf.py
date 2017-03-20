from ansible.plugins.action.template import ActionModule as TemplateModule
from ansible.errors import AnsibleError

try:
    from __main__ import display
except ImportError:
    from ansible.utils.display import Display
    display = Display()


class ActionModule(TemplateModule):
    ''' Nginx configuration file module '''

    def run(self, tmp=None, task_vars=None):
        result = {}
        src_file = self._task.args.get('src', None)
        src_filename_cleaned = src_file.replace('.j2', '')
        state = self._task.args.get('state', None)

        DEFAULT_DIRS = {
            'available': '/etc/nginx/sites-available',
            'enabled': '/etc/nginx/sites-enabled'
        }
        site_available_dir = self._templar.template(task_vars.get('nginx_sites_available_dir', DEFAULT_DIRS['available']))
        site_enabled_dir = self._templar.template(task_vars.get('nginx_sites_enabled_dir', DEFAULT_DIRS['enabled']))
        conf_available_path = '{}/{}'.format(site_available_dir, src_filename_cleaned)
        conf_enabled_sym_path = '{}/{}'.format(site_enabled_dir, src_filename_cleaned)

        if state == 'absent':
            r1 = self.remove_file(conf_enabled_sym_path, task_vars, tmp)
            r2 = self.remove_file(conf_available_path, task_vars, tmp)
        elif state == 'available':
            r1 = self.do_template(src_file, conf_available_path, task_vars, tmp)
            r2 = self.remove_file(conf_enabled_sym_path, task_vars, tmp)
        elif state == 'enabled':
            r1 = self.do_template(src_file, conf_available_path, task_vars, tmp)

            # Create the sites-enabled symlink via the File module now that the
            # site-available file has been created
            file_module_args = {
                'src': conf_available_path,
                'dest': conf_enabled_sym_path,
                'state': 'link'
            }
            r2 = self._execute_module(module_name='file', module_args=file_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False)
        else:
            raise AnsibleError("nginx module: {} is not a valid state. Choose one of [absent, enabled, available]".format(state))

        if r1.get('failed'):
            raise AnsibleError(r1)
        if r2.get('failed'):
            raise AnsibleError(r2)

        result.update({
            'nginx_conf': src_filename_cleaned,
            'changed': r1['changed'] or r2['changed'],
            'state': state
        })
        return result

    def remove_file(self, file_path, task_vars, tmp):
        file_module_args = {
            'path': file_path,
            'state': 'absent'
        }
        return self._execute_module(module_name='file', module_args=file_module_args, task_vars=task_vars, tmp=tmp, delete_remote_tmp=False)

    def do_template(self, src, dest, task_vars, tmp):
        ########################################################################
        # Populate the template file via the Template module's `run()` method.
        # Even though there is a way to call an external *module*, I couldn't
        # find a way to call an extenal *plugin*, and template is technically an
        # action plugin with an empty module.
        #
        # All Ansible action plugins look for parameters through self._task.
        # This means in order to call an external plugin, we have to alter
        # self._task. We'll keep a local copy of the current self._task and
        # restore the copy after the plugin has finished.
        ########################################################################
        orig_task_args = self._task.args.copy()

        template_args = self._task.args.copy()
        template_args.update({
            'src': src,
            'dest': dest
        })
        ## 'state' is an invalid param for the Template Module
        template_args.pop('state', None)

        self._task.args = template_args
        result = super(ActionModule, self).run(tmp, task_vars)
        self._task.args = orig_task_args

        return result
