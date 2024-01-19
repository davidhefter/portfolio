public class Node {
    private Point point;
    private Node parent;
    private int g;
    private int h;
    public Node(Point point, Node parent, int g, int h){
        this.point = point;
        this.parent = parent;
        this.g = g;
        this.h = h;
    }
    public int getG(){ return this.g; }
    public int getH(){ return this.h; }
    public int getF(){ return this.g + this.h; }
    public Point getPoint(){ return this.point; }
    public Node getParent(){ return this.parent; }
    public void adjustParent(Node newParent){
        if((newParent.g + distanceHeuristic(newParent.getPoint(), this.point)) < this.g) {
            this.g = newParent.g + distanceHeuristic(newParent.getPoint(), this.point);
            this.parent = newParent;
        }
    }
    public static int distanceHeuristic(Point p1, Point p2){
        int dX = Math.abs(p1.x - p2.x);
        int dY = Math.abs(p1.y - p2.y);
        int linear = Math.abs(dX-dY);
        int diagonal = Math.abs(Math.max(dX,dY) - linear);
        return (10*linear) + (14*diagonal);
    }
    public static boolean neighbors(Point p1, Point p2)   {
        return p1.x+1 == p2.x && p1.y == p2.y ||
                p1.x+1 == p2.x && p1.y+1 == p2.y ||
                p1.x == p2.x && p1.y+1 == p2.y ||
                p1.x-1 == p2.x && p1.y+1 == p2.y ||
                p1.x-1 == p2.x && p1.y == p2.y ||
                p1.x-1 == p2.x && p1.y-1 == p2.y ||
                p1.x == p2.x && p1.y-1 == p2.y ||
                p1.x+1 == p2.x && p1.y-1 == p2.y;
    }
}
