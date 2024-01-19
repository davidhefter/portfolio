import processing.core.PImage;

import java.util.List;

public class Sapling extends Plant{
    public static final String KIND = "SAPLING";
    private final String KEY = KIND.toLowerCase();
    public static final int NUM_PROPERTIES = 1;
    public static final int HEALTH_INDEX = 0;
    public static final double ACTION_ANIMATION_PERIOD = 1.000;
    public static final int HEALTH_LIMIT = 5;
    public Sapling(String id, Point position, List<PImage> images, int health) {
        super(id, position, images, health, ACTION_ANIMATION_PERIOD, ACTION_ANIMATION_PERIOD);
    }
    public boolean transform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        if (this.getHealth() <= 0) {
            Entity stump = new Stump(Stump.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Stump.KIND.toLowerCase()));

            world.removeEntity( scheduler,this);

            world.addEntity(stump);

            return true;
        } else if (this.getHealth() >= HEALTH_LIMIT) {
            Entity tree = new Tree(Tree.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(),imageStore.getImageList(Tree.KIND.toLowerCase()),
                    Functions.getIntFromRange(Tree.HEALTH_MAX, Tree.HEALTH_MIN),
                    Functions.getNumFromRange(Tree.ACTION_MAX, Tree.ACTION_MIN),
                    Functions.getNumFromRange(Tree.ANIMATION_MAX, Tree.ANIMATION_MIN));

            world.removeEntity(scheduler, this);

            world.addEntity(tree);
            ((ActionDoer)tree).scheduleActions(scheduler, world, imageStore);

            return true;
        }

        return false;
    }

    @Override
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler) {
        this.setHealth(this.getHealth()+1);
        if (!((Transform)this).transform( world, scheduler, imageStore)) {
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
        Entity skeleton = new Skeleton(Skeleton.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Skeleton.KIND.toLowerCase()), 0.2, 0.85);
        world.removeEntity( scheduler,this);
        world.addEntity(skeleton);
        ((ActionDoer)skeleton).scheduleActions(scheduler, world, imageStore);
        //EntityTransformer.transformToSkeleton(world, scheduler, imageStore, this);
        return true;
    }
}
