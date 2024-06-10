#!/usr/bin/env python
# -*- coding:utf-8 -*-


"""
/*******************************************************************************
Copyright (c) 1983-2021 Advantech Co., Ltd.
********************************************************************************
THIS IS AN UNPUBLISHED WORK CONTAINING CONFIDENTIAL AND PROPRIETARY INFORMATION
WHICH IS THE PROPERTY OF ADVANTECH CORP., ANY DISCLOSURE, USE, OR REPRODUCTION,
WITHOUT WRITTEN AUTHORIZATION FROM ADVANTECH CORP., IS STRICTLY PROHIBITED.

================================================================================
REVISION HISTORY
--------------------------------------------------------------------------------
$Log:  $
--------------------------------------------------------------------------------
$NoKeywords:  $
*/
/******************************************************************************
*
* Windows Example:
*    InstantAI.py
*
* Example Category:
*    AI
*
* Description:
*    This example demonstrates how to use Instant AI function.
*
* Instructions for Running:
*    1. Set the 'deviceDescription' for opening the device.
*    2. Set the 'profilePath' to save the profile path of being initialized device.
*    3. Set the 'startChannel' as the first channel for scan analog samples
*    4. Set the 'channelCount' to decide how many sequential channels to scan analog samples.
*
* I/O Connections Overview:
*    Please refer to your hardware reference manual.
*
******************************************************************************/
"""
import sys
sys.path.append('..')
from CommonUtils import kbhit
import time

from Automation.BDaq import *
from Automation.BDaq.InstantAiCtrl import InstantAiCtrl
from Automation.BDaq.BDaqApi import AdxEnumToString, BioFailed


import rospy
from std_msgs.msg import Float32MultiArray,Float32

deviceDescription = "USB-4716,BID#0"
profilePath = u"../../profile/DemoDevice.xml"

channelCount = 2
startChannel = 0

ret = ErrorCode.Success


pub = rospy.Publisher('chatter', Float32, queue_size=1)
pub_dt = rospy.Publisher('chatter_dt', Float32, queue_size=1)
rospy.init_node('talker', anonymous=True)
rate = rospy.Rate(1000)


# Step 1: Create a 'instantAiCtrl' for InstantAI function
# Select a device by device number or device description and specify the access mode.
# In this example we use ModeWrite mode so that we can fully control the device, including configuring, sampling, etc.
instanceAiObj = InstantAiCtrl(deviceDescription)
time1 = rospy.Time.now()
time2 = time1
for _ in range(1):
    instanceAiObj.loadProfile = profilePath   # Loads a profile to initialize the device

    # Step 2: Read samples and do post-process, we show data here.
    print("Acquisition is in progress, any key to quit!")
    list = Float32()
    list.data=0
    while not rospy.is_shutdown():
        # ret, scaledData = instanceAiObj.readDataF64(startChannel, channelCount)
        # if BioFailed(ret):
            # break
        # for i in range(startChannel, startChannel + channelCount):
            # print("Channel %d data: %10.6f" % (i, scaledData[i-startChannel]))
            # list.data = scaledData
        list.data=list.data + 0.001
        if list.data > 1:
            list.data = 0
            
        pub.publish(list)
        time1 = rospy.Time.now()
        pub_dt.publish((time1-time2).to_sec())
        time2 = time1
        rate.sleep()
        
instanceAiObj.dispose()

if BioFailed(ret):
    enumStr = AdxEnumToString("ErrorCode", ret.value, 256)
    print("Some error occurred. And the last error code is %#x. [%s]" % (ret.value, enumStr))

