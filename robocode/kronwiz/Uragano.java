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
	boolean stopRadarWobbling = false;  // indica se devo bloccare l'oscillazione del radar
	int radarWobblingDirection = 1;  // 1 = senso orario, -1 = senso antiorario
	double prevTargetEnergy = 0;  // energia del target rilevata durante la scansione precedente

	/**
	 * run: Uragano's default behavior
	 */
	public void run() {
		// Initialization of the robot should be put here

		setColors(Color.red,Color.blue,Color.green); // body,gun,radar

		// Robot main loop
		setAdjustRadarForGunTurn ( true );  // fa muovere il radar indipendentemente dal cannone e dal robot
		while ( true ) {
			if ( ! stopRadarWobbling ) {
				turnRadarRight ( radarWobblingDirection * 360 );
				// invertiamo la direzione di oscillazione a ogni giro
				radarWobblingDirection = radarWobblingDirection * -1;
			}
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
	public double computeBulletPower ( double targetDistance ) {
		double power = ( 600 - targetDistance ) / 200;
		if ( power <= 0 ) power = 0.1;
		return power;
	}

	/**
	 * normalizeAngle: normalizza un angolo nell'intervallo -360/+360
	 * 
	 * Se l'angolo passato come parametro è al di fuori dell'intervallo (in gradi)
	 * -360/360 viene riportato un questo intervallo.
	 * 
	 * NB: da valutare se sia meglio l'intervallo 0/360.
	 */
	public double normalizeAngle ( double angle ) {
		while ( angle >= 360 ) {
			angle = angle - 360;
		}

		while ( angle <= -360 ) {
			angle = angle + 360;
		}

		return angle;
	}

	/**
	 * onScannedRobot: What to do when you see another robot
	 */
	public void onScannedRobot(ScannedRobotEvent e) {
		// appena vedo un robot blocco l'oscillazione del radar (quella controllata
		// nel metodo "run")
		stopRadarWobbling = true;

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
		double targetEnergy = e.getEnergy ();  // energia del target

		/*
		 * Se c'è una variazione nell'energia del target può darsi che abbia sparato,
		 * così mi muovo per cercare di schivare il proiettile.
		 */
		if ( targetEnergy < prevTargetEnergy ) {
			turnRight ( 90 + targetBearing );
			ahead ( 60 * direction );			
		} else if ( targetDistance > 300 ) {
			// se sono troppo lontano mi avvicino
			turnRight ( targetBearing );
			ahead ( targetDistance - 200 );
			targetDistance -= 200;
		}

		prevTargetEnergy = targetEnergy;

		// mi giro sempre perpendicolarmente al target
//		turnRight ( 90 + targetBearing );


		// punto il cannone e sparo
		/*
		 * Scelgo l'angolo di rotazione più piccolo. Se l'angolo risultante è minore
		 * di 180 gradi utilizzo quello, altrimenti utilizzo l'angolo cosiddetto
		 * "esplementare", ovvero quello che sommato dà l'angolo giro perché in tal
		 * caso è lui ad essere minore. I valori assoluti tengono conto del fatto che
		 * gli angoli hanno un segno per indicare il verso di rotazione orario o antiorario,
		 * e il segno deve essere tolto dai conti; ma alla fine il segno deve essere
		 * ripristinato nell'ultima rotazione, altrimenti il cannone girerebbe sempre
		 * a sinistra anche quando dovrebbe girare a destra.
		 */
		double gunAngle = normalizeAngle ( heading - getGunHeading () + targetBearing );
		//out.println ( "gunAngle:" + gunAngle );
		if ( Math.abs ( gunAngle ) < 180 )
			turnGunRight ( gunAngle );
		else
			turnGunLeft ( Math.signum ( gunAngle ) * ( 360 - Math.abs ( gunAngle ) ) );

		// sparo
		fire( computeBulletPower ( targetDistance ) );

/*
		// mi muovo un po' avanti e un po' indietro
		if ( targetDistance <= 300 ) {
			ahead ( direction * 40 );
			steps++;
			if ( steps % 20 == 0 ) direction *= -1;
		}
*/

		// giro il radar verso il bersaglio per tenerlo sotto controllo (se ci riesco)
		double radarAngle = heading - getRadarHeading () + targetBearing;
		turnRadarRight ( radarAngle );

		// se ho ancora un robot nel radar questo interrompe il metodo e lo ricomincia da capo
		scan ();

		// quindi in teoria se arrivo qui significa che non ho visto alcun robot, perciò è
		// giusto far fare un giro al radar
		stopRadarWobbling = false;
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
