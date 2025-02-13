import {Text,View} from "react-native"
import { useContext } from "react"
import {AuthContext} from "../auth/authcontext"

export default function Home() {
    const authcontext = useContext(AuthContext!);

    if(!authcontext){
        return <Text>No context available</Text>;
    }

    const { user, setUser } = authcontext;

    
  return (
    <View>
      {user ? <Text>Welcome, {user.username}</Text> : <Text>Please log in</Text>}
    </View>
  );
}