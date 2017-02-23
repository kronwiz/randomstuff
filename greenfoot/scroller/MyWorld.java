import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)
import java.util.ArrayList;

/**
 * Write a description of class MyWorld here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class MyWorld extends World
{
    public int margineDestro = 0;
    public ArrayList blocchi = new ArrayList();
    // private int b_width = 0;
    
    /**
     * Constructor for objects of class MyWorld.
     * 
     */
    public MyWorld()
    {    
        // Create a new world with a cell size of 1x1 pixels.
        super(600, 400, 1);
        
        fill();
    }
    
    private void fill()
    {
        Blocco blocco = new Blocco(); // usato solo per recuperare le dimensioni
        int b_width = blocco.getImage().getWidth();
        int b_height = blocco.getImage().getHeight();

        margineDestro = ( getWidth() / b_width - 1 ) * b_width + b_width / 2;

        blocchi.clear(); // non si sa mai
        
        for ( int k = 0; k < ( getWidth() / b_width ); k++ ) {
            blocco = new Blocco();
            addObject ( blocco, b_width / 2 + b_width * k, getHeight() - b_height / 2 );
            blocchi.add(blocco);
        }
    }
    
    // public void act()
    // {
        // for ( int k = 0; k < blocchi.size(); k++ ) {
            // Blocco blocco = (Blocco) blocchi.get(k);
            // blocco.move(-1);
            
            // if ( blocco.getX() < ( b_width / 2 ) ) {
                // blocco.setLocation ( margineDestro, blocco.getY() );
            // }
        // }
    // }
}
