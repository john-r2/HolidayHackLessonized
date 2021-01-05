#!/bin/bash
declare -x LAST_ORDER
LAST_ORDER=''
# https://bash.cyberciti.biz/guide/Menu_driven_scripts
# A menu driven shell script sample template
## ----------------------------------
# Step #1: Define variables
# ----------------------------------
RED='\033[0;41;30m'
STD='\033[0;0;39m'
# ----------------------------------
# Step #2: User defined function
# ----------------------------------
pause() {
  read -r -p "Press [Enter] key to continue..." fackEnterKey
}

one() {
  cat /opt/castlemap.txt
  pause
}
two() {
  more /opt/coc.md
  pause
}
three() {
  cat /opt/directory.txt
  pause
}
four() {
  read -r -p "Enter your name (Please avoid special characters, they cause some weird errors)..." 
name
  if [ -z "$name" ]; then
    name="Santa\'s Little Helper"
  fi
  bash -c "/usr/games/cowsay -f /opt/reindeer.cow $name"
  pause
}
surprise(){
  cat /opt/plant.txt
  echo "Sleeping for 10 seconds.." && sleep 10
}
# function to display menus
show_menus() {
  clear
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo " Welcome to the North Pole!"
  echo "~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
  echo "1. Map"
  echo "2. Code of Conduct and Terms of Use"
  echo "3. Directory"
  echo "4. Print Name Badge"
  echo "5. Exit"
  echo
  echo
  echo "Please select an item from the menu by entering a single number."
  echo "Anything else might have ... unintended consequences."
  echo
}
# read input from the keyboard and take a action
read_options() {
  local choice
  read -r -p "Enter choice [1 - 5] " choice
  case $choice in
  1*) one ;;
  2*) two ;;
  3*) three ;;
  4*) four $choice ;;
  5) exit 0 ;;
  plant) surprise c;;
  *) echo -e "${RED}Error...${STD}" && sleep 2 ;;
  esac
}
# ----------------------------------------------
# Step #3: Trap CTRL+C, CTRL+Z and quit singles
# ----------------------------------------------
trap '' SIGINT SIGQUIT SIGTSTP

# -----------------------------------
# Step #4: Show opening message once
# ------------------------------------
echo
echo Welcome to our castle, we\'re so glad to have you with us!
echo Come and browse the kiosk\; though our app\'s a bit suspicious.
echo Poke around, try running bash, please try to come discover,
echo Need our devs who made our app pull/patch to help recover?
echo
echo "Escape the menu by launching /bin/bash"
echo
echo
read -n 1 -r -s -p $'Press enter to continue...'
clear
# -----------------------------------
# Step #5: Main logic - infinite loop
# ------------------------------------
while true; do
  show_menus
  read_options
done