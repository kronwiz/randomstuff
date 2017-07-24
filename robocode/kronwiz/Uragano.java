package kronwiz;
import robocode.*;
import java.awt.Color;

// API help : http://robocode.sourceforge.net/docs/robocode/robocode/Robot.html

/*
 * Articoli interessanti: http://mark.random-article.com/weber/java/robocode/
 */

/**
 * Uragano - a robot by AG
 */
public class Uragano extends Robot
{
	/**
	 * run: Uragano's default behavior
	 */
	public void run() {
		// Initialization of the robot should be put here

		// After trying out your robot, try uncommenting the import at the top,
		// and the next line:

		setColors(Color.red,Color.blue,Color.green); // body,gun,radar

		// Robot main loop
		setAdjustRadarForGunTurn ( true );  // fa muovere il radar indipendentemente dal cannone e dal robot
		while ( true ) {
			turnRadarRight ( 360 );
		}
	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		/*
		 * e.getBearing = angolo tra l'heading del robot e il target acquisito
		 * 
		 * Quindi per far ruotare il radar nella direzione del target occorre correggere
		 * con la differenza tra l'heading del robot e l'heading del radar.
		 * Stesso ragionamento per il movimento del cannone.
		 * Si usa sempre turn*Right perché se il risultato dell'operazione è negativo
		 * turn*Right muove correttamente il radar/cannone a sinistra invece che a destra.
		 */
		
		if ( e.getDistance () > 300 ) {
			turnRight ( e.getBearing () );
			ahead ( e.getDistance () - 300 );
		} else {
			turnGunRight ( getHeading () - getGunHeading () + e.getBearing () );
			fire(2);
		}

		turnRadarRight ( getHeading () - getRadarHeading () + e.getBearing () );
	}

	/**
	 * onHitByBullet: What to do when you're hit by a bullet
	 */
	public void onHitByBullet(HitByBulletEvent e) {
		// Replace the next line with any behavior you would like
		// back(10);
	}
	
	/**
	 * onHitWall: What to do when you hit a wall
	 */
	public void onHitWall(HitWallEvent e) {
		// Replace the next line with any behavior you would like
		back(20);
	}	
}
