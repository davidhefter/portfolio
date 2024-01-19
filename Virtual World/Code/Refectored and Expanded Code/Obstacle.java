import processing.core.PImage;

import java.util.List;

public class Obstacle extends ActionDoer implements Animate {
    public static final String KIND = "OBSTACLE";
    public static final int ANIMATION_PERIOD = 0;
    public static final int NUM_PROPERTIES = 1;
    private final String KEY = KIND.toLowerCase();

    private double animationPeriod;
    public Obstacle(String id, Point position, List<PImage> images, double animationPeriod){
        super(id, position, images);
        this.animationPeriod = animationPeriod;
    }
    public void nextImage(){
        this.setImageIndex(this.getImageIndex()+1);
    }
    @Override
    public double getAnimationPeriod(){
        return this.animationPeriod;
    }

    @Override
    public int getHealth() {
        return 0;
    }

    @Override
    public String getKey(){
        return KEY;
    }

    @Override
    public void scheduleActions(EventScheduler scheduler, WorldModel world, ImageStore imageStore) {
        scheduler.scheduleEvent(this, new Animation(this, 0), this.animationPeriod);
    }
}
