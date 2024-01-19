import processing.core.PImage;

import java.util.List;

public abstract class Entity {
    public static final int PROPERTY_KEY = 0;
    public static final int PROPERTY_ID = 1;
    public static final int PROPERTY_COL = 2;
    public static final int PROPERTY_ROW = 3;
    public static final int MIN_PROPERTIES = 4;



    private String id;
    private List<PImage> images;
    private int imageIndex;
    private Point position;

    public Entity(String id, Point position, List<PImage> images){
        this.id = id;
        this.images = images;
        this.imageIndex = 0;
        this.position = position;
    }
    public Entity(String id, Point position, List<PImage> images, int imageIndex){
        this.id = id;
        this.images = images;
        this.imageIndex = imageIndex;
        this.position = position;
    }



    public PImage getCurrentImage(){
        return this.images.get(this.imageIndex % this.images.size());
    }
    public void setPosition(Point position){
        this.position = position;
    }
    public String log(){
        return this.id.isEmpty() ? null :
                String.format("%s %d %d %d", this.id, this.position.x,
                        this.position.y, this.imageIndex);
    }




    public String getId(){ return this.id; }
    public List<PImage> getImages() { return images; }
    public int getImageIndex() {  return imageIndex; }
    public Point getPosition() {
        return position;
    }
    //public String getKind(){ return this.getKey().toUpperCase(); }
    public abstract String getKey();
    public abstract int getHealth();
    public void setImageIndex(int index){
        this.imageIndex=index;
    }
}
