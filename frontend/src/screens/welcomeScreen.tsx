import React from "react";
import { View, Text, StyleSheet, Image } from "react-native";
import { useNavigation } from "@react-navigation/native";
import { useEffect } from "react";
import { RootStackParamList } from "../types/naviType";
import { StackNavigationProp } from "@react-navigation/stack";
import Logo from "../components/Logo";

type WelcomeScreenNavigationProp = StackNavigationProp<
  RootStackParamList,
  "Welcome"
>;

export default function WelcomeScreen() {
  console.log("WelcomeScreen is loaded");

  const navigation = useNavigation<WelcomeScreenNavigationProp>();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigation.navigate("Signup");
    }, 2500);

    return () => clearTimeout(timer);
  }, [navigation]);

  return (
    <View className="flex-1 justify-center items-center bg-white">
      <Logo height={15} width={35} />

      <Text className="mt-4 text-green-700 text-5xl space-y-2 font-semibold">
        CROPXPERT
      </Text>
    </View>
  );
}
