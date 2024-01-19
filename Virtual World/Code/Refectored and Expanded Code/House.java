import processing.core.PImage;

import java.util.List;

public class House extends Entity {
    public static final String KIND = "HOUSE";
    public static final int NUM_PROPERTIES = 0;
    private final String KEY = KIND.toLowerCase();
    public House(String id, Point position, List<PImage> images){
        super(id, position, images);
    }

    @Override
    public int getHealth() {
        return 0;
    }

    @Override
    public String getKey(){
        return KEY;
    }
}
