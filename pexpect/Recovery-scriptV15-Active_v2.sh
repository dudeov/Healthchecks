while true;
do
# ############################################################################################################################## #
#                                               This is Recovery-Script15.Active.sh  											 #
# ############################################################################################################################## #
# 1. Script MONITOR the appearance of RIPD4 every 30 seconds to detect Soft errors (SER) in the chipset and recover from them.   #
# 2. This version adds a more frequent monitoring of RIPD4 to reduce overall impact.                                             #
# 3. We will trigger PFE RESTART when RIPD4 appear.      																		 #
# 4. The script will print in messages.log if there is a PFE restart.        													 #
# >. Note: For any further questions contact JTAC engineers. 														         	 #
# ############################################################################################################################## #
echo " ACTIVE MONITORING SCRIPT RUNNING "
date

# Command definition:
GENERAL="set bc bc "
COMMAND="show c"

# Let's have a check:  
cprod -A feb0 -c $GENERAL\"$COMMAND\" > /var/tmp/script/commandMonitor.txt
 
# Check if we are dropping IPV4 which is the first symptom seen on issue state.
RIPD4_APPEAR=$(cat /var/tmp/script/commandMonitor.txt | sed -e 's/^[ \t]*//' | grep RIPD4.cpu0 | awk '{print int($3) }')
echo "$RIPD4_APPEAR"

if [ -z "$RIPD4_APPEAR" ];then
{
echo "RIPD4 is empty, which is good - Just keep monitoring"
# We just sleep for 30 seconds, so far we are good.
sleep 30
}

else
{
# We seems to be in a bad situation here
echo "We are dropping RIPD4 and this is critical"
logger -p warning "RIPD4 appear - Hw looping state"
logger -p warning "The script is REBOOTING the FEB"
cli -c "restart feb"
#Sleep 4 minutes after the FEB restart , to avoid checking again too soon.
sleep 240
logger -p warning "DMA issue occurred, FEB automatically restarted"
}

fi
done