import processing.core.PImage;

import java.util.List;

public abstract class ActionDoer extends Entity {
    public ActionDoer(String id, Point position, List<PImage> images){
        super(id, position, images);
    }

    public void scheduleActions(EventScheduler scheduler, WorldModel world, ImageStore imageStore){
        Act act = (Act)this;
        scheduler.scheduleEvent(this, new Activity(this, world, imageStore), act.getActionPeriod());
        Animate animate = (Animate)this;
        scheduler.scheduleEvent(this, new Animation(this, 0), animate.getAnimationPeriod());
    }


}
