# UniBot
Discord Bot for the Universe Editing Server

Documentation updated April 22, 2021

# Commands

## User commands
### $plugins / $paste
Sends the plugin pastebin link
### $lumamatte / $luma
Sends the lumma matte shader
### $velocity / $velo
Sends a velocity tutorial
### $depth / $dof
Sends a dof tutorial
### $fovoptions \<fov> / $mcfov \<fov>
Converts the fov specified by the user to a numeric representation seen in Minecraft's options.txt
### $smoothvsharp / $svs
Sends a demonstration of smooth and sharp velocity
### $replaytutorial / $replay
Sends OE9's repaly mod tutorials
### $replaydownload / $rpmdl
Sends a link to ReplayMod's download page
### $ffmpeg
Sends OE9's ffmpeg installation graphics
### $logos / $intros
Sends a download link to Universe Editing logos
### $apply / $app
Sends a link to the Universe Editing application form
### $ratiotoresolutions \<width> \<height> / $r2r \<width> \<height>
Prints common resolutions in the specified aspect ratio
### $unibothelp / $h 
Sends a link to this page
### $socials \<member+ name> / $s <member+ name>
Prints socials of a Member+
### $ping
Sends "Pong."

## Trial/Member/Member+ Commands
### $updateyoutube \<youtube link> / $youtube \<youtube link>
Changes the youtube link listed on the roster [updates when admin runs $updateRoster]
### $checktrial / $check
Allows Trials to display when their Trial role will expire
### $updateSocials \<socials/message> / $us \<socials/message>
Updates the message that's sent when $socials is used
### $queue \<download link> / $q \<download link>
In #✅ready-to-upload-✅ channel allows members to queue an edit for uploading on Uni
### $updateName \<name> / $upname \<name>
Updates the name displayed on roster and the name used for $socials

## Admin Commands
### $clear \<n> / $c \<n>
Clears last n messages in the current channel
### $kick @user \<reason> / $k @user \<reason>
Kicks the user for a reason and notes it in a moderation log
### $ban @user \<reason> / $b @user \<reason>
Bans the user for a reason and notes it in a moderation log
### $mute @user \<reason> / $m @user \<reason>
Mutes the user for a reason and notes it in a moderation log
### $unmute @user / $um @user
Unmutes a user and notes it in a moderation log
### $promote @user [Trial/Member/Member+] / $p @user [Trial/Member/Member+]
Promotes the user to specified rank and adjusts roster/trial/member+ databases to reflect the change
### $addtoroster @user [Trial/Member/Member+] / $rosteradd @user [Trial/Member/Member+]
Manually adds the user to the roster [shouldn't need to be used]
### $removefromroster @user / $rosterremove @user
Manually removes the user from the roster [shouldn't need to be used]
### $updateRoster / $uproster
Prints roster in the current channel
### $expiretrials / $expire
Prints expired trials, removes them from the roster, and expires them in the trial database [does not remove trial role]
### $checktrial @Trial / $check @Trial
Prints the date when Trial's trial will expire
### $clearSocials @Member+
Removes a Member+'s socials displayed in $socials
