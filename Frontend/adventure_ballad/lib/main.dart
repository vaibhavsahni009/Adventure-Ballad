import 'package:flutter/material.dart';
import 'enter_name_page.dart';

void main() {
  runApp(AdventureBalladApp());
}

class AdventureBalladApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Adventure Ballad',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: EnterNamePage(),
    );
  }
}
