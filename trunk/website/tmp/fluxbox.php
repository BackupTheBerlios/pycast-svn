<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">

<html>
<head>
<title>iphitus</title>
<script src="http://aslan.no-ip.com/~iphitus/site/opera.js" type="text/javascript"></script>
</head>
<body>

<div class="container">
    <div class="top">
	   <?php require_once("site/title.php")?>
    </div>
    <div class="left">
        <?php require_once("site/navigation.php") ?>
    </div>
    <div class="main">
<h1>Unofficial Fluxbox FAQ</h1>
<h2>Making Fluxbox easy</h2>
<img src="http://aslan.no-ip.com/~iphitus/site/hr.png" alt="horizontal rule"/><br /><br />

<a href="#versions">What are the different fluxbox versions?</a><br />
<a href="#setwallpaper">How do I set my wallpaper?</a><br />
<a href="#rememberwall">How do I make fluxbox remember my wallpaper?</a><br />
<a href="#changestyle">How can I change my fluxbox style?</a><br />
<a href="#getstyle">Where can I get styles?</a><br />
<a href="#tooltrans">How do I make the toolbar and windows transparent?</a><br />
<a href="#menutrans">How do I make the menu or slit transparent?</a><br />
<a href="#installstyle">How do I install a style?</a><br />
<a href="#makestyle">How do I make a style?</a><br />
<a href="#shortcut">How do I bind keyboard shortcuts?</a><br />
<a href="#changemenu">How do I change my fluxbox menu?</a><br />
<a href="#icons">How do I get icons on my fluxbox desktop?</a><br />
<a href="#startup">How can I make programs startup when fluxbox starts?</a><br />
<a href="#startx">How do I start fluxbox from the command line?</a><br />
<a href="#slit">What is the slit?</a><br />
<a href="#dockapps">Where can I get dockapps for the slit?</a><br />
<a href="#toolbar">How can I change what's on my fluxbox toolbar?</a><br />
<a href="#clock">How can I change the format of the clock on the toolbar?</a><br />
<a href="#aa">How do I enable Anti-Aliased fonts?</a><br />
<a href="#tabs">What are fluxbox tabs and how do I use them?</a><br />
<a href="#borderless">How do I make windows borderless?</a><br />
<a href="#xorg">What do I do if I am having layering problems in Xorg 6.8</a><br />
<a href="#one">When will Fluxbox reach 1.0?</a><br /><br />


This FAQ applies to the current development series of Fluxbox, it was written using 0.9.10. If you dont have the developmental series you will find that many answers here will not help you. To find out what version of fluxbox you have, open a command line and write:
<h5>
fluxbox -version
</h5>
<a name="versions">&nbsp;</a>
<h3>What are the different fluxbox versions</h3>
<h2>0.1.14</h2>

This is the current "stable" version of fluxbox. It is no longer maintained. This is now out of date, it was released in late 2002, and I recommend you update to the latest in the 0.9.x (0.9.9 at writing) series.

<h2>0.9.x</h2>

This is the current development series of fluxbox. This is much much more feature rich than the older 0.1.14 series and is what I cover throughout this FAQ. It has newer features such as, transparency, pixmap themes, extra theme options as well as many many new additions to functionality, and speed. The 0.9.x series in my opinion, and in my experience, is more stable than the venerable 0.1.14 release. This is currently not considered the official stable release as it lacks in some documentation, translations, still has a handful of bugs to squash and new features to add.

<a name="setwallpaper">&nbsp;</a>
<h3>How do I set my wallpaper?</h3>

To set wallpapers in fluxbox, you need to use a special tool. Open up the command-line and type

<h5>fbsetbg /path/to/wallpaper.jpg</h5>

fbsetbg doesnt set the wallaper itself, it uses other programs to set it for you. The purpose of fbsetbg, is to pick the most appropriate program available to set the wallpaper. Not all wallpaper setters support transparency, so fbsetbg picks ones that support transparency over others. If you find that transparency is not working, do a fbsetbg -i and it will tell you if the wallpaper setter you have available doesnt support transparency.

Replace "/path/to/wallpaper.jpg" with the location of the image you want to set as the background. fbsetbg has an array of options, and they are passed:

<h5>fbsetbg -fctial /path/to/wallpaper.jpg</h5>

The main options you can pass to fbsetbg are below, you only need to pass one:
<pre>
-f - Set fullscreen wallpaper

-c - Set centered wallpaper

-t - Set tiled wallpaper

-a - Set wallpaper maximised with preserved aspect.

-i - Tell the user the program it is using to set the wallpaper and any pitfalls it might have.

-l - Set last wallpaper
</pre>
Other options can be found by reading:

<h5>man fbsetbg</h5>
<a name="rememberwall">&nbsp;</a>
<h3>How do I make fluxbox remember my wallpaper?</h3>

To make fluxbox remember your wallpaper, open up "~/.fluxbox/init" and find the line:

<h5>session.screen0.rootCommand:  </h5>

And replace it with

<h5>session.screen0.rootCommand:    fbsetbg -l   </h5>

This will make fluxbox remember your wallpaper by having fbsetbg set the last wallpaper.

<a name="menutrans">&nbsp;</a>
<h3>How do I make the menu or slit transparent?</h3>

One of the touted features of fluxbox is it's transparency abilities. They are not too complicated to change and can make some very cool eyecandy

You can change the level of transparency in the menu, or the menu alpha by right clicking to bring up the fluxbox menu then

<h5>Fluxbox menu > Fluxbox > Configure > Menu Alpha</h5>

The slit transparency can be found by right clicking the slit or by looking in

<h5>Fluxbox menu > Fluxbox > Configure > Slit > Alpha</h5>

You can click on the value there to adust it. "0" is fully transparent, "255" is solid. Values in between have varying levels of transparency.

If you find that the menu's transparency does not take effect immediately, try restarting fluxbox.

If restarting fluxbox doesn't fix your problem and you set the transparency to "0", try setting it to "1" and restarting fluxbox. There was a bug in some development versions of fluxbox that made the setting of "0", act like "255".
<a name="tooltrans">&nbsp;</a>
<h3>How do I make the toolbar and windows transparent?</h3>

To change the transparency levels of the toolbar, window borders or the slit, you will need to modify your theme. This will change the appearance of the theme and may not be something you wish to do.

First, open the theme's configuration file with your favourite text editor.

This will usually be at

<h5>/home/username/.fluxbox/style/stylename/theme.cfg</h5>

Or if it was made using the older format:

<h5>/home/username/.fluxbox/style/stylename</h5>

Find these lines and adjust the numeric values to your liking.
<pre>
toolbar.alpha: 100

window.alpha: 255
</pre>
Save the theme and then restart fluxbox from your fluxbox menu


<a name="getstyle">&nbsp;</a>
<h3>Where can I get styles?</h3>
Themes, or styles as they are known for fluxbox can be found all over the internet, a good search on Google will turn up a lot of links. Here are some good sites.
<ul>
<li><a href="http://www.themedepot.org/showarea.php4?area=23">http://www.themedepot.org/showarea.php4?area=23</a></li>
<li><a href="http://fluxbox.org/download/themes/">http://fluxbox.org/download/themes/</a></li>
<li><a href="http://geekgirl.bz">http://geekgirl.bz</a></li>
<li><a href="http://www.deviantart.com">http://www.deviantart.com</a></li>
<li><a href="http://themes.freshmeat.net/browse/962/?topic_id=962">http://themes.freshmeat.net/browse/962/?topic_id=962</a></li>
<li><a href="http://www.xs4all.nl/~hanb/software/fluxbox/styles">http://www.xs4all.nl/~hanb/software/fluxbox/styles</a></li>
</ul>
Not to long ago there used to be a popular site called fluxmod, it was the home of fluxbox theming and held some of the best pixmap themes around. Unfortnately because of technical problems, it was shut down. You can get a tarball (tar.gz) of all the themes from:
<br />
<br />
<a href="http://aslan.no-ip.com/~iphitus/downloads/themes/Fluxmod-TheAshes.tar.bz2">Fluxmod-TheAshes.tar.bz2</a>
<a name="changestyle">&nbsp;</a>
<h3>How can I change my fluxbox style?</h3>

You can change styles in fluxbox by going into
<h5>Fluxbox menu > Fluxbox > Styles</h5>

Then selecting whichever one takes your fancy
<a name="installstyle">&nbsp;</a>
<h3>How do I install a style?</h3>
Themes for fluxbox can be distributed and installed in many different ways. The most common way of distributing a fluxbox theme is inside a .tar.gz or .tar.bz2.

For most themes, it is fine to just, download the theme to your /home/username directory and then extract it.
<br />
You extract tar.gz with:

<h5>tar -zxvf theme.tar.gz</h5>

And tar.bz2 with

<h5>tar -jxvf theme.tar.bz2</h5>

The style should appear in the menu. If the style does not appear in your menu, take a look in your /home/username directory. If you see a folder called styles or pixmaps then your theme takes an extra step to install.
<pre>
cd ~/.fluxbox/

tar -zxvf ../theme.tar.gz
</pre>
or
<pre>
tar -jxvf ../theme.tar.bz2
</pre>
The style should be in your menu now. If it isn't, as a last ditch effort, restart fluxbox.
<a name="makestyle">&nbsp;</a>
<h3>How do I make a style?</h3>

If you are interested in creating themes for fluxbox, it is very easy. Grab your favourite text editor, hack some existing theme's file or head over to asenchi's tutorial:
<br />To view it in man format
<h5>man fluxstyle</h5>

or online here: <a href="http://aslan.no-ip.com/~iphitus/misc/themes.html">http://aslan.no-ip.com/~iphitus/misc/themes.html</a>
<a name="shortcut">&nbsp;</a>
<h3>How do I bind keyboard shortcuts?</h3>
To setup keyboard shortcuts, you can use one of the following solutions
<ul>
<li>xbindkeys <a href="http://hocwp.free.fr/xbindkeys/xbindkeys.html">http://hocwp.free.fr/xbindkeys/xbindkeys.html</a></li>
<li>fluxkeys from fluxconf <a href="http://devaux.fabien.free.fr/flux/">http://devaux.fabien.free.fr/flux/</a></li>
<li>Manually</li>
</ul>
The fluxbox man page covers the manual way excellently<br /><br />
<div style="margin-left: 40px; background-color: #cfdbe8; display: block;">
You  can  customise  Fluxbox'  key handling through the ~/.fluxbox/keys file.  The file takes the format of :
<pre>
&lt;modifier&gt; &lt;key&gt; [...] :&lt;operation&gt;
</pre>

In the example below, Mod1 is the 'Alt' key on the PC keyboard and Mod4 is one of the three extra keys on a pc104 branded with a sickening corporate logo.
<pre>
# Fluxbox keys file.
# Any line starting with a # is a comment.
Mod1 Tab :NextWindow
Mod1 F1 :Workspace 1
Mod1 F2 :Workspace 2
Mod1 F3 :Workspace 3
Mod1 F4 :Workspace 4
Mod1 F5 :Workspace 5
Mod1 F6 :Workspace 6
Mod1 F7 :Workspace 7
Mod1 F8 :Workspace 8
Mod1 F9 :Workspace 9
Mod4 b :PrevWorkspace
Mod4 c :Minimize
Mod4 r :ExecCommand rxvt
Mod4 v :NextWorkspace
Mod4 x :Close
Mod4 m :RootMenu
Control n Mod1 n :NextTab
None Print :ExecCommand import -window root '%Y-%m-%d_$wx$h.png'; xmessage 'snapshot done'
</pre>
As you can see from the last line, keybinds can be chained in a fashion similar to emacs keybindings.
Commands  are  caseinsensitive, workspace numbering starts at "1", some commands have synonyms.
</div><br />
To get a list of all the available commands, look in the man page. You can access the man page though the command line by typing:
<pre>man fluxbox</pre>

The man page is also <a href="fluxman.html">available online</a>.
<a name="changemenu">&nbsp;</a>
<h3>How do I change my fluxbox menu?</h3>
There are two ways of changing your fluxbox menu, they are:
<ul>
<li>fluxmenu from fluxconf <a href="http://devaux.fabien.free.fr/flux/">http://devaux.fabien.free.fr/flux/</a></li>
<li>Manually</li>
</ul>
The fluxbox manual has an extensive section on doing it manually, and it isnt very hard. You can access the man page though the command line by typing:
<pre>man fluxbox</pre>

The man page is also <a href="fluxman.html">available online</a>.


<a name="icons">&nbsp;</a>
<h3>How do I get icons on my fluxbox desktop?</h3>
Check out these great tutorials by ikaro:
<ul>
<li>idesk <a href="http://ikaro.dk/content.php?article.16">http://ikaro.dk/content.php?article.16</a></li>
<li>rox pager <a href="http://ikaro.dk/content.php?article.4">http://ikaro.dk/content.php?article.4</a></li>
</ul>


<a name="startup">&nbsp;</a>
<h3>How can I make programs startup when fluxbox starts?</h3>
There are two methods of starting a program on startup.
<ul>
<li>/home/username/.fluxbox/apps</li>
<li>/home/username/.fluxbox/startup</li>
</ul>
It doesnt matter which of these two methods you use, most distros support the startup file, and the apps file is supported on every distro.
<br /><br />
<h2>startup</h2>

You can put commands to run whatever programs you want in here. It is a great place to put programs like your dockapps, fbdesk, idesk, gdesklets, torsmo or any other programs you like to have running. The advantage it has over the apps file is that it's a shell script, allowing you to do more.
An example of this is:

<h5>gkrellm &amp;
aterm &amp;
</h5>
<h2>apps</h2>
The apps file uses a different syntax to the startup file. To make a program startup, in the apps file add

<h5>[startup] {programname}</h5>

An example of this is:
<h5>[startup] {gkrellm}</h5>
<h5>[startup] {aterm}</h5>


<a name="startx">&nbsp;</a>
<h3>How do I start fluxbox from the command line?</h3>

If you want to use startx to start fluxbox from the command line, or you have been dumped out to a command line without X, this is how you can start X running fluxbox.

<h5>echo exec startfluxbox > ~/.xinitrc</h5>

Then run

<h5>startx</h5>


And X will start, running fluxbox and any programs you set to load in your startup files.
<a name="slit">&nbsp;</a>
<h3>What is the slit?</h3>

The slit is a special dock in fluxbox where you can put applications called dockapps. It can be located on any side of the screen, and you can change this and many other features by right clicking it and changing them. These options are also available in the main fluxbox menu under:

<h5>Fluxbox menu > Fluxbox > Configure > Slit</h5>

<a name="dockapps">&nbsp;</a>
<h3>Where can I get dockapps for the slit?</h3>
You can find many dockapps to put in this area, at:
<br /><br />
<a href="www.dockapps.org">www.dockapps.org</a>


<h3>How can I change what's on my fluxbox toolbar?</h3><a name="toolbar">&nbsp;</a><br />
In your /home/username/.fluxbox/init change the line, you may add or remove whatever you wish from there.

<h5>session.screen0.toolbar.tools:</h5>

<h3>How can I change the format of the clock on the toolbar?</h3><a name="clock">&nbsp;</a><br />
The clock on the toolbar is set with the format of the unix date command. This is stored in your /home/username/.fluxbox/init in:
<h5>session.screen0.strftimeFormat:</h5>
You may get valid formats for this from

<h5>man date</h5>

<a name="aa">&nbsp;</a>
<h3>How do I enable Anti-Aliased fonts?</h3>

To enable Anti-Aliased fonts, enable the following option in the Fluxbox menu:

<h5>Fluxbox menu > Fluxbox > Configure > Anti-Aliasing</h5>
<a name="tabs">&nbsp;</a>
<h3>What are fluxbox tabs and how do I use them?</h3>

Fluxbox is able to tab windows, just like tabbed browsing in Mozilla browsers. This can be a great way of saving space, organising windows, and its a great feature to show off to your GNOME or KDE friends. These tabs are integrated into the titlebar of a program and are very easy to work with.

To tab one program with another, use your middle mouse button (left and right mouse buttons together if you dont have one) on the titlebar and drag it onto the window you want to have the program tabbed with. It should automatically tab them together and you can choose either one by clicking on it as you would in Mozilla. To untab a program, middle click it's title and drag it away, making sure it is not over any other windows.

<a name="borderless">&nbsp;</a>
<h3>How do I make windows borderless?</h3>

<h2>Temporary</h2>

To set a program to be borderless temporarily, add this line to your /home/username/.fluxbox/keys:

<h5>mod1 t :toggledecor</h5>

Then using the main fluxbox menu, reload the configuration.

Once you have done that, select the program you want to have temporary borderlessness and type:

<h5>alt-t</h5>

<h2>Permanent</h2>

If you dont already have one, you will need to create a /home/username/.fluxbox/apps and then add the following lines to it:
<pre>
[app] (aterm)

[Deco] {NONE}

[end]</pre>

Replace aterm, with the program you wish to make borderless, then restart fluxbox from its menu.
<a name="xorg">&nbsp;</a>
<h3>What do I do if I am having layering problems in Xorg 6.8</h3>
If you are having layer problems in fluxbox, where windows aren't raising and lowering as you would like, fix it by changing the following.
<pre>Right click slit > Layer > Desktop</pre>
<a name="one">&nbsp;</a>
<h3>When will Fluxbox reach 1.0?</h3>
When it needs to. At the moment there is still some work to be done.
        <?php require_once("site/end.php") ?>	
    </div>
</div>


</body>

</html>
