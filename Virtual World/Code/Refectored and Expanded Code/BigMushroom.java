import processing.core.PImage;

import java.util.List;

public class BigMushroom extends Entity implements DudeTransform, FairyTransform, ClickEventTransform{
    public static final int NUM_PROPERTIES = 0;
    public static final String KIND = "BIGMUSHROOM";
    private final String KEY = KIND.toLowerCase();
    public BigMushroom(String id, Point position, List<PImage> images){
        super(id, position, images);
    }

    @Override
    public int getHealth() {
        return 0;
    }
    public String getKey(){
        return this.KEY;
    }

    @Override
    public boolean dudeTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        /*Entity fairy = new Fairy(Fairy.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(Fairy.KIND.toLowerCase()), 0.123, 0.123);
        world.removeEntity( scheduler,this);
        world.addEntity(fairy);
        ((ActionDoer)fairy).scheduleActions(scheduler, world, imageStore);*/
        EntityTransformer.transformToFairy(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean fairyTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        /*Entity sapling = new Sapling(Sapling.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(),
                imageStore.getImageList(Sapling.KIND.toLowerCase()), 0);
        world.removeEntity(scheduler, this);
        world.addEntity(sapling);
        ((ActionDoer)sapling).scheduleActions(scheduler, world, imageStore);*/
        EntityTransformer.transformToSapling(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean clickTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        /*Entity sapling = new Sapling(Sapling.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(),
                imageStore.getImageList(Sapling.KIND.toLowerCase()), 0);
        world.removeEntity(scheduler, this);
        world.addEntity(sapling);
        ((ActionDoer)sapling).scheduleActions(scheduler, world, imageStore);*/
        EntityTransformer.transformToSapling(world, scheduler, imageStore, this);
        return true;
    }


}
