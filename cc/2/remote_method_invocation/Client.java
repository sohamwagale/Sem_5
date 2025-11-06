import java.rmi.*;

public class Client {
    public static void main(String args[]) {
        try {
            Hello h = (Hello) Naming.lookup("rmi://<SERVER_IP>/HelloService"); // Replace with Server's IP
            System.out.println(h.sayHello());
        } catch (Exception e) {
            System.out.println("Client error: " + e);
        }
    }
}
