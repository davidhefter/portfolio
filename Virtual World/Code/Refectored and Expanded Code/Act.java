public interface Act{
    public void executeActivity(WorldModel world, ImageStore imageStore, EventScheduler scheduler);
    public double getActionPeriod();
}
