import processing.core.PImage;

import java.util.List;

public class Stump extends Entity implements ClickEventTransform, WizardTransform, FairyTransform {
    public static final int NUM_PROPERTIES = 0;
    public static final String KIND = "STUMP";
    private final String KEY = KIND.toLowerCase();
    public Stump(String id, Point position, List<PImage> images){
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
    public boolean clickTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(bigmush);
        //EntityTransformer.transformToBigMushroom(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean wizardTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(bigmush);
        //EntityTransformer.transformToBigMushroom(world, scheduler, imageStore, this);
        return true;
    }
    @Override
    public boolean fairyTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){

        Entity sapling = new Sapling(Sapling.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(),
                imageStore.getImageList(Sapling.KIND.toLowerCase()), 0);
        world.removeEntity(scheduler, this);
        world.addEntity(sapling);
        ((ActionDoer)sapling).scheduleActions(scheduler, world, imageStore);
        //EntityTransformer.transformToSapling(world, scheduler, imageStore, this);
        return true;
    }
}
