package linkedList;

public class LinkedListTester {

    public static void main(String[] args) {
        Node head = new Node(10);
        Node t1 = new Node(30);
        Node t2 = new Node(20);

        head.next = t1;
        t1.next = t2;
    }
}
