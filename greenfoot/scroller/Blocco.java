import greenfoot.*;  // (World, Actor, GreenfootImage, Greenfoot and MouseInfo)

/**
 * Write a description of class Blocco here.
 * 
 * @author (your name) 
 * @version (a version number or a date)
 */
public class Blocco extends Actor
{
    private int width = getImage().getWidth();
    private int height = getImage().getHeight();
    
    /**
     * Act - do whatever the Blocco wants to do. This method is called whenever
     * the 'Act' or 'Run' button gets pressed in the environment.
     */
    public void act() 
    {
       move(-1);
       
       if ( getX() < width / 2 ) {
           MyWorld world = (MyWorld) getWorld();
           setLocation( world.margineDestro, getY() );
       }
    }    
}
