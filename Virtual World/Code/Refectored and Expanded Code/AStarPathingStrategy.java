import java.util.*;
import java.util.function.BiPredicate;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class AStarPathingStrategy implements PathingStrategy {


    public List<Point> computePath(Point start, Point end,
                                   Predicate<Point> canPassThrough,
                                   BiPredicate<Point, Point> withinReach,
                                   Function<Point, Stream<Point>> potentialNeighbors) {
        List<Point> path = new LinkedList<>();
        List<Node> closedList = new LinkedList();
        List<Node> openList = new LinkedList();

        final var ref = new Object() {
            Node currentNode = new Node(start, null, 0, Node.distanceHeuristic(start, end));
        };
        openList.add(ref.currentNode);
        while (true) {
            // find neighbors that are in the cardinal directions, aren't occupied, and aren't in closedList
            List<Node> newNeighbors = potentialNeighbors.apply(ref.currentNode.getPoint())
                    .filter(canPassThrough)
                    .filter((pt) -> !closedList.stream().map(Node::getPoint).toList().contains(pt))
                    .map((pt) -> new Node(
                            pt,
                            ref.currentNode,
                            ref.currentNode.getG() + Node.distanceHeuristic(ref.currentNode.getPoint(), pt),
                            Node.distanceHeuristic(pt, end)
                        ))
                    .toList();
            // Add new nodes to add to openList and modify existing duplicates if present
            newNeighbors.forEach((neighborNode)->{
                        if (!openList.stream().map(Node::getPoint).toList().contains(neighborNode.getPoint())){
                            openList.add(neighborNode);
                        }else {
                            openList.forEach((openNode) -> {
                                if (openNode.getPoint().equals(neighborNode.getPoint())) {
                                    openNode.adjustParent(ref.currentNode);
                                }
                            });
                        }
                    });
            closedList.add(ref.currentNode);
            openList.remove(ref.currentNode);
            // Once there are no more accessed nodes left to check
            if (!openList.isEmpty()){
                ref.currentNode = openList.stream().sorted(Comparator.comparingInt(Node::getF)).toList().get(0);
                if(withinReach.test(ref.currentNode.getPoint(), end)){
                    Node tail = ref.currentNode;
                    while (tail.getParent() != null){
                        path.add(0, tail.getPoint());
                        tail = tail.getParent();
                    }
                    return path;
                }
            }else if(!closedList.isEmpty()){
                return path;
            }


        }
            /*
            + Filtered list containing neighbors you can actually move to
            + Check if any of the neighbors are beside the target
            + set the g, h, f values
            - add them to open list if not in open list
            + add the selected node to close list
          return path*/

    }

}
