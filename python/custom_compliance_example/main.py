# -*- mode: python; python-indent: 4 -*-
import ncs
from ncs.application import Service
from ncs.dp import Action
# Jinja imports
import os
from jinja2 import Environment
from jinja2 import FileSystemLoader
# example: https://routebythescript.com/creating-network-configurations-with-jinja/


# ---------------
# ACTIONS EXAMPLE
# ---------------
class DoubleAction(Action):
    @Action.action
    def cb_action(self, uinfo, name, kp, input, output, trans):
        self.log.info('action name: ', name)
        self.log.info('action input.number: ', input.number)

        service = ncs.maagic.get_node(trans, kp)
        root = ncs.maagic.get_root(trans)
        # netbox_server = root.netbox_server[service.netbox_server]
        trans.maapi.install_crypto_keys()
        with ncs.maapi.Maapi() as m:
            with ncs.maapi.Session(m, 'admin', 'python'):
                with m.start_write_trans() as t:
                    # Create new service object from a writeable transaction
                    writeable_service = ncs.maagic.get_node(t, service._path)
                    template = ncs.template.Template(writeable_service)

                    devices = []
                    root = ncs.maagic.get_root(t)
                    writeable_service = ncs.maagic.get_node(t, service._path)
                    template = ncs.template.Template(writeable_service)
                    vars = ncs.template.Variables()
                    #sanity check
                    device_cdb = root.devices.device["dist-rtr01"]
                    device_cdb.name = "NOT-dist-rtr01"
                    output.result = device_cdb.name
                    # end
                    # root.custom_compliance_example__custom_compliance_example.create("first")
                    # output.result = type(root.custom_compliance_example__custom_compliance_example["first"].device  

                    # root.custom_compliance_example__custom_compliance_example["first"].report_categories = ["banner"]
                    cp = ncs.maapi.CommitParams()
                    cp.dry_run_native()
                    r = t.apply_params(True, cp)
                    t.apply()


# /custom_compliance_example[name='first']/device [ dist-rtr01 ]
# /custom_compliance_example[name='first']/report_categories [ banner interfaces ]

        # credit: https://github.com/NSO-developer/Cisco-NSO-MPLS-VPN-service-reconciliation-example/blob/14a311db4727baaab8dd3f038aa3064610b1f39f/packages/l3vpn/python/action.py#L178
        # with ncs.maapi.single_write_trans('admin', 'python') as t:
        #             # Create new service object from a writeable transaction
        #             writeable_service = ncs.maagic.get_node(t, service._path)
        #             template = ncs.template.Template(writeable_service)

        #             devices = []
        #             root = ncs.maagic.get_root(t)
        #             root.custom_compliance_example__custom_compliance_example
                    ## end block
        #             # I will first get the list of all CPEs
        #             cpe_names = root.ncs__devices.device_group['C'].device_name
                    
        #             for cpe in cpe_names:
        #                 self.log.info("Analysing CPE: " + str(cpe))
        #                 cpe_device = root.ncs__devices.device[cpe]
                        
        #                 # I will now check if bgp exist and if
        #                 # if exits, it belogns to a VPN
        #                 if(cpe_device.config.ios__router.bgp):
        #                     endpoint_name = "discovered_%s" % cpe
        #                     self.log.info("BGP Found")
        #                     cpe_bgp = cpe_device.config.ios__router.bgp
                            
        #                     for asn in cpe_bgp:
        #                         endpoint_asn=asn.as_no
                                
        #                         for neighbor in asn.neighbor:
        #                             cpe_neighbor = neighbor.id
                            
        #                     # Now I will check if policy is been configured
        #                     if cpe_device.config.ios__policy_map:
        #                         policy_maps = cpe_device.config.ios__policy_map
                                
        #                         choices = ['BRONZE', 'SILVER', 'GOLD']
                                
        #                         for policy_map in policy_maps:
        #                             if policy_map.name in choices:
        #                                 endpoint_qos = policy_map.name
        #                             else:
        #                                 service_name = policy_map.name
        #                                 endpoint_bandwidth = policy_map.ios__class['class-default'].shape.average.bit_rate
                            
        #                     for interface in cpe_device.config.ios__interface.GigabitEthernet:
        #                         if (interface.description == "%s local network" % service_name):
        #                             endpoint_interface = "GigabitEthernet%s" % interface.name
        #                             int_address= interface.ip.address.primary.address
        #                             int_mask = interface.ip.address.primary.mask
        #                             interface = ipaddress.IPv4Interface(unicode('%s/%s' % (int_address,int_mask), "utf-8"))
        #                             endpoint_network = str(interface.network)
                            
        #                     service_rd = self.get_rd(root,service_name,endpoint_asn)
                            
        #                     changed_services.append(service_name)
                            
        #                     # Now I can go and create the endpoint
                            
        #                     if service_name not in root.l3vpn__vpn.l3vpn:
        #                         root.l3vpn__vpn.l3vpn.create(service_name)
                            
        #                     service = root.l3vpn__vpn.l3vpn[service_name]
        #                     service.route_distinguisher = service_rd
                            
        #                     # This should be different
                            
        #                     if endpoint_name not in service.endpoint:
        #                         service.endpoint.create(endpoint_name)
                            
        #                     endpoint = service.endpoint[endpoint_name]
        #                     endpoint.as_number = endpoint_asn
        #                     endpoint.bandwidth = endpoint_bandwidth
        #                     endpoint.ce_device = cpe
        #                     endpoint.ce_interface = endpoint_interface
        #                     endpoint.ip_network = endpoint_network
        # ## end of block

        #                     # now lets see what I want to perform the commit dry-run
        #                     # I use native format to detect changes in device
        #                     input_dr = root.ncs__services.commit_dry_run.get_input()
        #                     input_dr.outformat = 'native'
        #                     dry_output = root.ncs__services.commit_dry_run(input_dr)
                            
        #                     output.result += "Commit Dry Run Device Changes: \n"
        #                     # Let me check that no device will be modified:
                            
        #                     if len(dry_output.native.device) == 0:
        #                         output.status = True
        #                         output.result += "No Changes \n"
        #                     else:
        #                         for device in dry_output.native.device:
        #                             output.result += "Device: %s \n" % device.name
        #                             output.result += str(device.data)
        #                             output.result += "\n"
                            
        #                     output.result += "Commit Dry Run Service Changes: \n"
        # template_output = j2_template_wrapper(template_service_name="wan",intf="Ethernet1/0",intdscr="WAN_byJinja",ip="10.1.1.1",
        #                   mask="255.255.255.252", qospol="200MB_SHAPE",bgpasn="65456",
        #                   bgpnip="10.1.1.2",remasn="65499")
        # output.result = template_output



def j2_template_wrapper(template_service_name, **kwargs):
    """
    adapted from Santiago's code:
    https://github.com/NSO-developer/service-launcher/blob/d0dc2a41315d5ac6dd8aca0d78a10b14610ff63d/web_ui/api_controller.py
    :param template_service_name: jinja template to be used
    :param kwargs: arguments to be replaced in the jinja template
    :return:
    """
    DIR_PATH = os.path.dirname(os.path.realpath(__file__))
    env = Environment(loader=FileSystemLoader(DIR_PATH + '/templates'))
    template = env.get_template(template_service_name + '.j2')
    rendered = template.render(**kwargs)
    return rendered

# ------------------------
# SERVICE CALLBACK EXAMPLE
# ------------------------
class ServiceCallbacks(Service):

    # The create() callback is invoked inside NCS FASTMAP and
    # must always exist.
    @Service.create
    def cb_create(self, tctx, root, service, proplist):
        self.log.info('Service create(service=', service._path, ')')

        vars = ncs.template.Variables()
        vars.add('DUMMY', '127.0.0.1')
        template = ncs.template.Template(service)
        template.apply('custom_compliance_example-template', vars)

    # The pre_modification() and post_modification() callbacks are optional,
    # and are invoked outside FASTMAP. pre_modification() is invoked before
    # create, update, or delete of the service, as indicated by the enum
    # ncs_service_operation op parameter. Conversely
    # post_modification() is invoked after create, update, or delete
    # of the service. These functions can be useful e.g. for
    # allocations that should be stored and existing also when the
    # service instance is removed.

    # @Service.pre_lock_create
    # def cb_pre_lock_create(self, tctx, root, service, proplist):
    #     self.log.info('Service plcreate(service=', service._path, ')')

    # @Service.pre_modification
    # def cb_pre_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')

    # @Service.post_modification
    # def cb_post_modification(self, tctx, op, kp, root, proplist):
    #     self.log.info('Service premod(service=', kp, ')')


# ---------------------------------------------
# COMPONENT THREAD THAT WILL BE STARTED BY NCS.
# ---------------------------------------------
class Main(ncs.application.Application):
    def setup(self):
        # The application class sets up logging for us. It is accessible
        # through 'self.log' and is a ncs.log.Log instance.
        self.log.info('Main RUNNING')

        # Service callbacks require a registration for a 'service point',
        # as specified in the corresponding data model.
        #
        self.register_service('custom_compliance_example-servicepoint', ServiceCallbacks)

        # When using actions, this is how we register them:
        #
        self.register_action('custom_compliance_example-action', DoubleAction)

        # If we registered any callback(s) above, the Application class
        # took care of creating a daemon (related to the service/action point).

        # When this setup method is finished, all registrations are
        # considered done and the application is 'started'.

    def teardown(self):
        # When the application is finished (which would happen if NCS went
        # down, packages were reloaded or some error occurred) this teardown
        # method will be called.

        self.log.info('Main FINISHED')
