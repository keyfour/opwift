#!/bin/bash
#
# OpenWrt wireless setup test
#
# Send uci commands via telnet and check result on local wireless interface
#
# Usage:
#
# openwift.sh [host promt] [host address]
#
# @author: Aleksandr Karpov <keyfour13@gmail.com>
# @version: 0.1


#SSID to setup
SSID="OpenWrt"

#Target wlan index
TWLAN=0

#Local wireless interface
WLAN="wlan5"

#Wait for rebooting in seconds
WAIT=120

#OpenWrt host promt
[[ "$1" ]] && { PROMT=$1; } || { PROMT="root@OpenWrt:/# "; }

#OpenWrt host
[[ "$2" ]] && { HOST=$2; } ||  { HOST=192.168.1.1; }

#Associative array where key is channel and value is frequency
#TODO: add more frequencies
declare -A FREQUENCIES=( [34]=5170 [36]=5180 [38]=5190 [40]=5200 )

#Send uci commands via telnet
# @parameters:
#   commands: commands in quotas to send
function send_by_telnet() {
  python telnet.py $HOST $PROMT $1

}

#Check SSID by scaning
# @paremeters:
#   ssid: string ssid value
function checkSSID() {
  result = $(sudo iw dev $WLAN scan | grep "SSID: $1")
  [[ ! $result ]] && { echo "Error on SSID checking!"; exit 1; } || echo "Done!"
}

#Check frequency by scanning
# @paremeters:
#   ssid: string ssid value
#   freq: integer frequency value,
function checkFrequency() {
  result = $(sudo iw dev $WLAN scan | grep "freq: $1")
  [[ ! $result ]] && { echo "Error on SSID checking!"; exit 1; } || echo "Done!"
}

echo "Setup SSID: $SSID"
send_by_telnet "\"uci set wireless.@wifi-iface[$TWLAN].ssid=\"$SSID\" && uci commit && reboot\""
[[ $? != 0 ]] && exit 1
echo "Wait for device rebooting..."
sleep $WAIT
echo "Check SSID: $SSID"
checkSSID $SSID

for channel in "${!FREQUENCIES[@]}"; do
  echo "Set channel $channel"
  send_by_telnet "\"uci set wireless.@wifi-device[$TWLAN].channel=$channel && uci commit && reboot\""
  [[ $? != 0 ]] && exit 1
  echo "Wait for device rebooting"
  sleep $WAIT
  checkFrequency() $SSID ${FREQUENCIES[$channel]}
done;
