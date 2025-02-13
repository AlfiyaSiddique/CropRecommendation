import React from "react";
import { View, Text, Image, TextInput, TouchableOpacity } from "react-native";
import { FontAwesome, Feather } from "@expo/vector-icons";
import axios from "axios";
import { NativeStackScreenProps } from "@react-navigation/native-stack";
import { RootStackParamList } from "../types/naviType";
import { Linking } from "react-native";
import Logo from "../components/Logo";
import { AuthContext } from "../auth/authcontext";
import { useState, useContext } from "react";
import AsyncStorage from "@react-native-async-storage/async-storage";
import { baseUrl } from "@env";

type Props = NativeStackScreenProps<RootStackParamList, "Login">;

export default function LoginScreen({ navigation }: Props) {
  const authContext = useContext(AuthContext);

  if (!authContext) {
    return <Text>Loading...</Text>;
  }

  const { setUser } = authContext;

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleLogin = async () => {
    try {
      const API_URL = `${baseUrl}:5000/auth/login`;

      console.log("attempting to login");

      const res = await axios.post(API_URL, {
        email: email,
        password: password,
      });

      console.log("Recived res in login :", res.data.user);

      const { access_token } = res.data;

      if (access_token) {
        console.log("Access token received:", access_token);
        setUser(res.data.user);
        await AsyncStorage.setItem("access_token", access_token);
        navigation.reset({
          index: 0,
          routes: [{ name: "Home" }],
        });
      }
    } catch (err) {
      console.log(err);
      alert("Error while loggin in");
    }
  };

  const handleNavigate = async () => {
    navigation.navigate("Signup");
  };

  return (
    <View className="bg-white flex flex-1 p-8 justify-evenly  ">
      <Logo height={10} width={20} />

      {/* form section  */}
      <View className="flex-1   justify-evenly">
        <View className="mb-6 items-start">
          <Text className="text-4xl font-semibold text-center">Welcome!</Text>
          <Text className="text-center text-gray-500 font-[20px] mt-2">
            Signin to to continue
          </Text>
        </View>

        <View className="space-y-4 ">
          <View className="flex-row items-center mb-5 border border-gray-400 pl-2 rounded-lg bg-gray-100">
            <FontAwesome name="user" size={20} color="gray" />
            <TextInput
              placeholder="Email"
              className="flex-1 ml-3"
              value={email}
              onChangeText={setEmail}
            />
          </View>

          <View className="flex-row items-center mb-1 border border-gray-400 pl-2 rounded-lg bg-gray-100">
            <Feather name="lock" size={20} color="gray" />
            <TextInput
              placeholder="Password"
              secureTextEntry
              className="flex-1 ml-3"
              value={password}
              onChangeText={setPassword}
            />
          </View>
          <TouchableOpacity
            className="bg-[#6fca3a] p-3  rounded-lg mt-10 items-center"
            style={{ width: "60%", alignSelf: "center" }}
            onPress={handleLogin}
          >
            <Text className="text-white font-semibold text-2xl">Sign in</Text>
          </TouchableOpacity>
        </View>

        {/* OR Section */}
        <View className="flex-row items-center my-4">
          <View className="flex-1 h-px bg-gray-500" />
          <Text className="mx-4 text-black text-2xl">or</Text>
          <View className="flex-1 h-px bg-gray-500" />
        </View>

        <TouchableOpacity className="flex-row  p-3 rounded-lg items-center justify-center">
          <Image
            source={require("../../assets/google.png")}
            style={{ width: 28, height: 30, marginRight: 10 }}
          />
          <Text className="text-gray-700">Log in with Google</Text>
        </TouchableOpacity>

        <View className="mt-5 flex-row justify-center">
          <Text className="text-gray-500">Don't have an account? </Text>
          <TouchableOpacity>
            <Text
              className="text-blue-500 font-semibold"
              onPress={handleNavigate}
            >
              Sign up
            </Text>
          </TouchableOpacity>
        </View>
      </View>
    </View>
  );
}
