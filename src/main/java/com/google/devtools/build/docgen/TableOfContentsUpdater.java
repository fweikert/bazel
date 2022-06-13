// Copyright 2022 The Bazel Authors. All rights reserved.
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//    http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.
package com.google.devtools.build.docgen;

import java.io.FileInputStream;
import java.io.FileWriter;
import org.yaml.snakeyaml.Yaml;
import com.google.devtools.common.options.OptionsParser;

public class TableOfContentsUpdater {
    public static void main(String[] args) {
        OptionsParser parser =
        OptionsParser.builder().optionsClasses(TableOfContentsOptions.class).build();
        parser.parseAndExitUponError(args);
        TableOfContentsOptions options = parser.getOptions(TableOfContentsOptions.class);

        if (options.help) {
            printUsage();
            Runtime.getRuntime().exit(0);
        }

        if (options.inputPath.isEmpty()
            || options.outputPath.isEmpty()
            || options.version.isEmpty()
            || options.baseUrl.isEmpty()
            || options.maxReleases < 1) {
            printUsage();
            Runtime.getRuntime().exit(1);
        }


        for (Package pkg : Package.getPackages()) {
            System.out.println(pkg);
        }
/*
        System.out.printf("i %s\no %s\nv %s\n", options.inputPath, options.outputPath, options.version);
        Yaml yaml = new Yaml();
        Object data = yaml.load(new FileInputStream(options.inputPath));
        System.out.println(data);
        yaml.dump(data, new FileWriter(options.outputPath)); */
    }

    private static void printUsage() {
        System.err.println(
            "Usage: toc-updater -i src_toc_path -o dest_toc_path -v version [-m max_releases] [-b base_url] [-h]\n\n"
                + "Reads the input TOC, adds an entry for the specified version and saves the new TOC at the specified location.\n");
      }
}