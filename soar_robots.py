#! /usr/bin/env python3

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
#члены класса робот

# add method to print debug messages from Soar
agent.RegisterForPrintEvent(sml.smlEVENT_PRINT,
                            cb_print_soar_message,
                            None)

# print all messages
agent.ExecuteCommandLine("watch 5")

# load .soar file in kernel
agent.ExecuteCommandLine("source robots.soar")

agent.RunSelf(1)
# get input link
input_link = agent.GetInputLink()

# get data from classes in robots.py??? and create inputs

#ЦИКЛ

robot_link = agent.CreateStringWME(input_link,
                                   'far_away',
                                   'r1')
# execute processing
agent.RunSelf(2)

# get output link
output_link = agent.GetOutputLink()

# get output
if output_link != None:
    try:
        result_output_wme = output_link.FindByAttribute("target", 0)
        target = result_output_wme.GetValueAsString()
    except AttributeError:
        print("error") #error
else:
    print("error")
    
    
print(target)


# destroy agent and kernel
kernel.DestroyAgent(agent)
kernel.Shutdown()
