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
	int direction = 1;  // 1 = in avanti, qualunque sia la direzione, -1 = indietro
	int steps = 0;

	/**
	 * run: Uragano's default behavior
	 */
	public void run() {
		// Initialization of the robot should be put here

		setColors(Color.red,Color.blue,Color.green); // body,gun,radar

		// Robot main loop
		setAdjustRadarForGunTurn ( true );  // fa muovere il radar indipendentemente dal cannone e dal robot
		while ( true ) {
			turnRadarRight ( 360 );
		}
	}

	/**
	 * computeBulletPower: calcola la potenza di fuoco
	 * 
	 * Un proiettile può essere sparato con un'energia tra 0.1 e 3.0
	 * Si muove a una velocità di: 20 - (3 * bulletPower)
	 * Fa un danno pari a: (bulletPower * 4) + (max(0, bulletPower - 1) * 2)
	 * Se colpisce il nemico restituisce un'energia pari a: 3 * bulletPower
	 * Dopo aver sparato il cannone si surriscalda di: 1 + (bulletPower / 5)
	 * 
	 * L'oggetto Rules contiene metodi che restituiscono il risultato di questi calcoli
	 * tenendo conto anche di alcuni parametri che possono essere modificati per ogni
	 * battaglia.
	 * 
	 * Al normale tasso di raffreddamento di 0.1 a turno questo significa che per sparare di
	 * nuovo il robot deve aspettare ceiling((1 + (bulletPower / 5)) * 10) turni prima di sparare
	 * di nuovo.
	 */
	public double computeBulletPower () {
		return 2;
	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		/*
		 * e.getBearing = restituisce angolo tra l'heading del robot e il target acquisito
		 * 
		 * Quindi per far ruotare il radar nella direzione del target occorre correggere
		 * con la differenza tra l'heading del robot e l'heading del radar.
		 * Stesso ragionamento per il movimento del cannone.
		 * Si usa sempre turn*Right perché se il risultato dell'operazione è negativo
		 * turn*Right muove correttamente il radar/cannone a sinistra invece che a destra.
		 */

		double targetBearing = e.getBearing ();  // posizione del target (angolo) rispetto al mio heading
		double heading = getHeading ();  // mia direzione
		double targetDistance = e.getDistance ();  // distanza del target

		// se sono troppo lontano mi avvicino
		if ( targetDistance > 300 ) {
			turnRight ( targetBearing );
			ahead ( targetDistance - 200 );
		}

		// mi giro sempre perpendicolarmente al target
		turnRight ( 90 + targetBearing );

		// punto il cannone e sparo		
		turnGunRight ( heading - getGunHeading () + targetBearing );
		fire( computeBulletPower () );

		// mi muovo un po' avanti e un po' indietro
		if ( targetDistance <= 300 ) {
			ahead ( direction * 40 );
			steps++;
			if ( steps % 20 == 0 ) direction *= -1;
		}

		// giro il radar verso il bersaglio per tenerlo sotto controllo (se ci riesco)
		turnRadarRight ( heading - getRadarHeading () + targetBearing );

		scan ();
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
		// se tocco un muro inverto la direzione di marcia
		direction *= -1;
	}	
}
