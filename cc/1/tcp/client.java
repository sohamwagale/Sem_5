
import java.util.*;
import java.net.*;
import java.io.*;

class tcpclient {

    public static void main(String args[]) {
        try {
            Socket s1 = new Socket("192.168.87.62", 1520);

            DataInputStream dis;
            DataOutputStream dos;
            InputStream is;
            OutputStream os;

            is = s1.getInputStream();
            os = s1.getOutputStream();
            dis = new DataInputStream(is);
            dos = new DataOutputStream(os);

            Scanner sc = new Scanner(System.in);
            String str;
            do {

                System.out.println("Data to send: ");
                str = sc.nextLine();
                dos.writeUTF(str);
                System.out.println("Data Received:");
                str = dis.readUTF();
                System.out.println(str);
            } while (!str.equals("STOP"));
            sc.close();
            s1.close();
        } 
        catch (Exception e) {
        }
    }
}
