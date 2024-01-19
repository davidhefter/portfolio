import processing.core.PImage;

import java.util.List;

public abstract class Plant extends ActionDoer implements Act, Animate, Transform, ClickEventTransform, WizardTransform {
    private double animationPeriod;
    private double actionPeriod;
    private int health;
    public Plant(String id, Point position, List<PImage> images, int health,
                 double animationPeriod, double actionPeriod){
        super(id, position, images);
        this.health = health;
        this.animationPeriod = animationPeriod;
        this.actionPeriod = actionPeriod;
    }
    public void decrementHealth(){
        this.health--;
    }
    @Override
    public double getActionPeriod(){
        return this.actionPeriod;
    }
    @Override
    public void nextImage(){
        this.setImageIndex(this.getImageIndex()+1);
    }
    @Override
    public double getAnimationPeriod(){
        return this.animationPeriod;
    }
    @Override
    public int getHealth(){
        return this.health;
    }
    public void setHealth(int health){ this.health = health; }

    @Override
    public boolean clickTransform(WorldModel world, EventScheduler scheduler, ImageStore imageStore){
        Entity bigmush = new BigMushroom(BigMushroom.KIND.toLowerCase() + "_" + this.getId(), this.getPosition(), imageStore.getImageList(BigMushroom.KIND.toLowerCase()));
        world.removeEntity( scheduler,this);
        world.addEntity(bigmush);
        //EntityTransformer.transformToBigMushroom(world, scheduler, imageStore, this);
        return true;
    }


}
