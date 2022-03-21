#!/usr/bin/env python3

import sys

# function to print Soar output
def cb_print_soar_message(mid, user_data, agent, message):
    print(message.strip() + '\n')

# load Soar library
sys.path.append('/opt/Soar/out')
import Python_sml_ClientInterface as sml

# create processing kernel
kernel = sml.Kernel.CreateKernelInCurrentThread()
agent = kernel.CreateAgent("agent")

# add method to print debug messages from Soar
agent.RegisterForPrintEvent(sml.smlEVENT_PRINT,
                            cb_print_soar_message,
                            None)
# print all messages
agent.ExecuteCommandLine("watch 5")

# load .soar file in kernel
agent.ExecuteCommandLine("source example.soar")

# get input and output links
input_link = agent.GetInputLink()
output_link = agent.GetOutputLink()

# add some data in input link as triples:
# (<input-link> data <agent1_description>)
# (<agent1_description> ki:track_id ki:agent1)
# (<agent1_description> rdf:type ki:robot)
# (<agent1_description> ki:size ki:big)
"""
agent_link = agent.CreateIdWME(input_link, 'data')
track_id_link = agent.CreateStringWME(agent_link,
                                      'ki:track_id',
                                      'ki:agent1')
type_link = agent.CreateStringWME(agent_link,
                                  'rdf:type',
                                  'ki:robot')
size_link = agent.CreateStringWME(agent_link,
                                  'ki:size',
                                  'ki:big')
"""
#tiger_link = agent.CreateStringWME(input_link,
                                 # 'obj',
                                  #'tiger')
squirell_link = agent.CreateStringWME(input_link,
                                  'obj',
                                  'squirell')


# execute processing
agent.RunSelf(2)

# destroy agent and kernel
kernel.DestroyAgent(agent)
kernel.Shutdown()
