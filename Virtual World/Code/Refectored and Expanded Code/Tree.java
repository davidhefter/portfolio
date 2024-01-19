import processing.core.PImage;

import java.util.List;

public class Tree extends Plant{
    public static final String KIND = "TREE";
    public static final int NUM_PROPERTIES = 3;
    public static final int ANIMATION_PERIOD = 0;
    public static final int ACTION_PERIOD = 1;
    public static final int HEALTH = 2;
    private final String KEY = KIND.toLowerCase();


    public static final double ANIMATION_MAX = 0.600;
    public static final double ANIMATION_MIN = 0.050;
    public static final double ACTION_MAX = 1.400;
    public static final double ACTION_MIN = 1.000;
    public static final int HEALTH_MAX = 3;
    public static final int HEALTH_MIN = 1;

    public Tree(String id, Point position, List<PImage> images, int health,
                double animationPeriod, double actionPeriod) {
        super(id, position, images, health, animationPeriod, actionPeriod);
    }
    @Override
    public boolean transform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        if (this.getHealth() <= 0) {
            Entity stump = new Stump(Stump.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(),imageStore.getImageList(Stump.KIND.toLowerCase()));
            world.removeEntity(scheduler, this);
            world.addEntity(stump);
            return true;
        }
        return false;
    }

    @Override
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler) {
        if (!((Transform)this).transform(world, scheduler, imageStore)) {

            scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.getActionPeriod());
        }
    }


    @Override
    public String getKey(){
        return KEY;
    }

    @Override
    public void scheduleActions(EventScheduler scheduler, WorldModel world, ImageStore imageStore) {
        scheduler.scheduleEvent(this, new Activity(this, world, imageStore), this.getActionPeriod());
        scheduler.scheduleEvent(this, new Animation(this, 0), this.getAnimationPeriod());
    }
    @Override
    public boolean wizardTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(bigmush);
        //EntityTransformer.transformToBigMushroom(world, scheduler, imageStore, this);
        return true;
    }

}
