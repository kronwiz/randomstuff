#package require Tk

source "./sprite_def_image.tcl"

set KW_WIDTH "width"
set KW_HEIGHT "height"
set KW_TO "to"
set KW_IN "in"
set KW_COSTUME "costume"

set ERR_OBJECT_NAME_EMPTY "Object name cannot be empty"
set ERR_OBJECT_NAME_EXISTS {Object name must be unique. The name \"$name\" already exists}
set ERR_OBJECT_NAME_UNKNOWN {Object with name \"$name\" doesn't exist}

set __STAGE__ {}
set __OBJTREE__ {}


proc wait {{how_long 1} {unit "milliseconds"}} {
	global __TK_WAIT__

	if {$unit eq "seconds"} {
		set how_long [expr {$how_long * 1000}]
	}
	after $how_long set __TK_WAIT__ &
	#vwait __TK_WAIT__
	tkwait variable __TK_WAIT__
	unset __TK_WAIT__
}

proc shift_args {params} {
	# removes the unnecessary preposition if there's any at the beginning of params
	# and returns the "clean" list of the remaining parameters
	global KW_TO KW_IN

	if {[lindex $params 0] in [list $KW_TO $KW_IN]} {
		lrange $params 1 end
	} else {
		return $params
	}
}

proc get_obj_by_name {name} {
	# returns the object with name "name" from the object tree or an error
	# if there's no such object
	global __OBJTREE__
	global ERR_OBJECT_NAME_UNKNOWN

	try {
		set obj [dict get $__OBJTREE__ $name]
	} on error {} {
		return -code error [subst -nocommands $ERR_OBJECT_NAME_UNKNOWN]
	}
	return $obj
}

proc new {what name args} {
	global __STAGE__ SPRITE_DEF_IMAGE __OBJTREE__
	global KW_WIDTH KW_HEIGHT KW_COSTUME
	global ERR_OBJECT_NAME_EMPTY ERR_OBJECT_NAME_EXISTS

	if {[string trim "$name"] eq ""} {return -code error $ERR_OBJECT_NAME_EMPTY}
	if [dict exists $__OBJTREE__ $name] {return -code error [subst -nocommands $ERR_OBJECT_NAME_EXISTS]}

	set obj [dict create\
		id 0\
		name $name\
		type $what\
		x 0\
		y 0\
		width 0\
		height 0\
		canvas_ ""\
		image_ ""\
		images ""\
		direction 90]

	dict set __OBJTREE__ $name $obj

	switch $what {
		stage {
			set wk [lsearch -exact $args $KW_WIDTH]
			set width [expr {$wk == -1 ? 640 : [lindex $args $wk+1]}]
			set hk [lsearch -exact $args $KW_HEIGHT]
			set height [expr {$hk == -1 ? 480 : [lindex $args $hk+1]}]
			dict set __OBJTREE__ $name width $width
			dict set __OBJTREE__ $name height $height

			set c [canvas .stage -height $height -width $width]
			pack $c
			dict set __OBJTREE__ $name canvas_ $c
			set __STAGE__ $c
		}

		sprite {
			set ck [lsearch -exact $args $KW_COSTUME]
			if {$ck == -1} {
				# if not specified use the default costume
				set costname __DEFAULT_COSTUME__
			} else {
				set costname [lindex $args $ck+1]
			}
			set costume [dict get $__OBJTREE__ $costname]  ;#FIXME: check for existence
			set images [dict get $costume images]
			set img [$__STAGE__ create image 50 50 -image [lindex $images 0] -anchor nw]
			dict set __OBJTREE__ $name image_ $img
		}

		costume {
			if {[llength $args] > 0} {
				for {set t 0} {$t < [llength $args]} {incr t} {
					#set img [image create photo -file [lindex $args $t]]  ;# NB: no name
					set img [pyimage create photo -file [lindex $args $t]]
					lappend images $img
				}
			} else {
				set img [image create photo -data $SPRITE_DEF_IMAGE]  ;# NB: no name
				#set img [pyimage create photo -data $SPRITE_DEF_IMAGE]
				lappend images $img
			}
			dict set __OBJTREE__ $name images $images
		}
	}

	return $obj
}

new costume __DEFAULT_COSTUME__ "./squirrel.png"

proc go {name to x {y 0}} {
	global __STAGE__ __OBJTREE__
	global ERR_OBJECT_NAME_UNKNOWN

	try {
		set obj [dict get $__OBJTREE__ $name]
	} on error {} {
		return -code error [subst -nocommands $ERR_OBJECT_NAME_UNKNOWN]
	}

	lassign [shift_args [list $to $x $y]] x y
	dict set __OBJTREE__ $name x $x
	dict set __OBJTREE__ $name y $y
	$__STAGE__ moveto [dict get $obj image_] $x $y
	wait  ;# always needed to avoid to freeze the Tk event loop
}

proc let {name what to {val 0}} {
	global __STAGE__ __OBJTREE__

	set obj [get_obj_by_name $name]
	lassign [shift_args [list $to $val]] val
	dict set __OBJTREE__ $name $what $val
	if {$what eq "x"} {
		set x $val
		set y ""
	} else {
		set x ""
		set y $val
	}
	$__STAGE__ moveto [dict get $obj image_] $x $y
	wait
}

proc point {name in direction {degrees 0}} {
	global __STAGE__ __OBJTREE__

	set obj [get_obj_by_name $name]
	lassign [shift_args [list $in $direction $degrees]] direction degrees
	dict set __OBJTREE__ $name direction $degrees
	# Image rotation articles:
	# http://blog.tcl.tk/4022  Photo image rotation
	# http://blog.tcl.tk/38709  Rotate TkPhoto Image
	# http://www.freedomenv.com/TkGooies/CODEpages/IMAGEtools/rotateImage_on2ndCanvas/rotate_image_on2ndCanvas.htm  FE 'tkGooie' Utilities 'IMAGEtools' group
}

proc repeat {times body} {
	for {set t 0} {$t < $times} {incr t} {
		uplevel 1 $body
	}
}


proc sposta {s} {
	go $s to 210 100
}

proc test {} {
	new stage s
	new costume squirrel
	new sprite a costume squirrel
	#new sprite a

	# prova di chiamata a una procedura
	sposta a


	for {set t 0} {$t < 200} {incr t} {
		go a to [expr {10+$t}] 20
		#go a [expr {10+$t}] 20
	}

	set t 0
	repeat 200 {
		incr t
		go a to 209 [expr {20+$t}]
		wait 10 ;# milliseconds
	}

	let a x to 20
	let a y to 20
}

test


# redefining proc example
#
#rename proc _proc
#
#_proc proc {name arglist body} {
#    if {![string match ::* $name]} {
#        #not already an 'absolute' namespace path
#        #qualify it so that traces can find it
#        set name [uplevel 1 namespace current]::[set name]
#    }
#    _proc $name $arglist $body
#
#
# Bella introduzione a Tcl di Antirez: http://antirez.com/articoli/tclmisunderstood.html
#
