import processing.core.PImage;

import java.util.List;
import java.util.function.BiPredicate;

public abstract class Mover extends ActionDoer implements Act, Animate {
    private double animationPeriod;
    private double actionPeriod;
    private PathingStrategy pStrategy;
    public Mover(String id, Point position, List<PImage> images,
                    double animationPeriod, double actionPeriod, PathingStrategy pStrategy){
        super(id, position, images);
        this.animationPeriod = animationPeriod;
        this.actionPeriod = actionPeriod;
        this.pStrategy = pStrategy;
    }
    public void nextImage(){
        this.setImageIndex(this.getImageIndex()+1);
    }
    @Override
    public double getAnimationPeriod(){
        return this.animationPeriod;
    }
    public double getActionPeriod(){
        return this.actionPeriod;
    }

    //public abstract Point nextPosition(WorldModel world, Point destPos);
    public abstract Point nextPosition(WorldModel world, Point destPos);

    public abstract boolean moveTo(WorldModel world, Entity target, EventScheduler scheduler);

    @Override
    public int getHealth() {
        return 0;
    }

    @Override
    public void scheduleActions(EventScheduler scheduler, WorldModel world, ImageStore imageStore) {
        scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.actionPeriod);
        scheduler.scheduleEvent(this, new Animation(this, 0), this.animationPeriod);
    }
}
