@0xecc23a6ce1dbd595;

# using Java = import "java.capnp";
# $Java.package("org.ericsson2017.protocol.test");
# $Java.outerClassname("RequestClass");

# using Cxx = import "/capnp/c++.capnp";
# $Cxx.namespace("ericsson2017::protocol::test");

using import "Bugfix.capnp".Bugfix;


struct Request {
    union {
        login : group {
            team @0 : Text;
            hash @1 : Text;
        }
        bugfix @2 : Bugfix;
    }
}
